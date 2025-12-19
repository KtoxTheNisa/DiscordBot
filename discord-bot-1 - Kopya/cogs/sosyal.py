import config
import discord
from discord.ext import commands
import asyncio
import random
import time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont 
from utils import parse_duration

# progress bar seviye gostergeci
def progressBar(percent):
    
    dolu = int(percent / 10)
    return f"[{'🟥' * dolu}{'⬛' * (10 - dolu)}]"

async def create_ship_image(u1, u2):
    #aavtarar icin
    a1 = u1.avatar.replace(format="png", size=128) if u1.avatar else u1.default_avatar.replace(format="png", size=128)
    a2 = u2.avatar.replace(format="png", size=128) if u2.avatar else u2.default_avatar.replace(format="png", size=128)
    
    d1 = BytesIO(await a1.read())
    d2 = BytesIO(await a2.read())
    
    i1 = Image.open(d1).convert("RGBA").resize((128, 128))
    i2 = Image.open(d2).convert("RGBA").resize((128, 128))
    
    bg = Image.new("RGBA", (350, 150), (44, 47, 51, 255))
    bg.paste(i1, (20, 11), mask=i1)
    bg.paste(i2, (202, 11), mask=i2)
    
    draw = ImageDraw.Draw(bg)
    draw.ellipse((148, 50, 198, 100), fill=(255, 0, 0, 255))
    
    fb = BytesIO()
    bg.save(fb, "PNG")
    fb.seek(0)
    return fb

class Sosyal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def fal(self, ctx):
        # veritabanına gerek yok bunda oylesine
        word = random.choice(config.FAL_SOZLERI)
        embed = discord.Embed(title="🔮 FALCI BACI", description=f"*{word}*", color=discord.Color.purple())
        embed.set_thumbnail(url="https://emojigraph.org/media/apple/crystal-ball_1f52e.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def askolcer(self, ctx, member: discord.Member):
        if member == ctx.author: return await ctx.send("Kendine mi aşıksın?")
        async with ctx.typing():
            percent = random.randint(0, 100)
            
            # yuzdelige gore yorum seciyoruz
            selected = next((x for x in config.ASK_DURUMLARI if percent <= x["limit"]), config.ASK_DURUMLARI[-1])
            try:
                #yardımcı fonksiyonlar kullanıyrzu
                img_file = await create_ship_image(ctx.author, member)
                file = discord.File(fp=img_file, filename="love.png")
                
                embed = discord.Embed(title="💘 AŞK ANALİZİ", description=f"{ctx.author.mention} ❤️ {member.mention}", color=selected["renk"])
                embed.add_field(name=f"Uyum: %{percent}", value=progressBar(percent))
                embed.add_field(name="Yorum", value=selected["yorum"])
                embed.set_image(url="attachment://love.png")
                embed.set_thumbnail(url=selected["gif"])
                await ctx.send(file=file, embed=embed)
            except Exception as e:
                 await ctx.send(f"{config.EMOJIS.get('error', '❌')} Resim oluşturulurken hata oluştu.")

    @commands.command()
    async def evlen(self, ctx, member: discord.Member):
        if member == ctx.author or member.bot: return await ctx.send("Hata.")
        
        guild_id, target_id, user_id = ctx.guild.id, ctx.author.id, member.id
        
        user_data = await self.bot.db.get_user_data(guild_id, user_id)
        target_data = await self.bot.db.get_user_data(guild_id, target_id)

        # zaten evli mi
        if user_data['partner_id'] or target_data['partner_id']: 
            return await ctx.send("Zaten evlisiniz.")
        
        if user_data['xp'] < 500: 
            return await ctx.send(f"💍 **Paran Yok!** 500 XP lazım.")
        
        await ctx.send(f"💍 {member.mention}, {ctx.author.mention} evlenmek istiyor! kabul ediyosan `evet` yaz.")
        try:
            await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == member and m.channel == ctx.channel and m.content.lower() == "evet")
            
            #db e gönderdik
            await self.bot.db.add_xp(guild_id, user_id, -500)
            await self.bot.db.set_partner(guild_id, user_id, target_id) 
            await self.bot.db.set_partner(guild_id, target_id, user_id)
            
            await ctx.send("🎉 **EVLENDİNİZ!**")
        except asyncio.TimeoutError: 
            await ctx.send("💔 Cevap gelmedi.")
            
    @commands.command()
    async def bosan(self, ctx):
        guild_id, user_id = ctx.guild.id, ctx.author.id
        
        user_data = await self.bot.db.get_user_data(guild_id, user_id)
        pid = user_data['partner_id']
        
        if not pid: return await ctx.send("Zaten bekarsın.")
        if user_data['xp'] < 200: return await ctx.send("Boşanma davası 200 XP.")
        
        await self.bot.db.add_xp(guild_id, user_id, -200)
        # partneri siliyoruz dbten fonks aldık
        await self.bot.db.divorce_partner(guild_id, user_id, pid)
        
        await ctx.send("💔 **Boşandın.**")

    @commands.command()
    async def rep(self, ctx, member: discord.Member):
        if member.id == ctx.author.id or member.bot: return
        
        guild_id, user_id, target_id = ctx.guild.id, ctx.author.id, member.id
        
        giver_data = await self.bot.db.get_user_data(guild_id, user_id)
        last_rep = giver_data['last_rep'] or 0
        
        # database'deki add_rep metodu hem rep'i artırıyor hem de cooldown'ı kaydediyor
        if time.time() - last_rep > 86400:
            # database'deki add_rep metodu "giver_user" ve "taker_user" IDlerini ister
            await self.bot.db.add_rep(guild_id, user_id, target_id)
            
            await ctx.send(f"⭐ **+REP!** {ctx.author.mention} -> {member.mention}")
        else:
             await ctx.send("⏳ Günde 1 kez rep verebilirsin.")

    @commands.command()
    async def sirbirak(self, ctx, *, secret: str):
        try: await ctx.message.delete()
        except: pass
        
        guild_id, user_id = ctx.guild.id, ctx.author.id
        
        await self.bot.db.add_secret(guild_id, secret)
        await self.bot.db.add_xp(guild_id, user_id, 50)
        
        await ctx.send("🤫 Sırrın kasaya atıldı. **+50 XP**", delete_after=5)

    @commands.command()
    async def siroku(self, ctx):
        guild_id, user_id = ctx.guild.id, ctx.author.id
        
        user_data = await self.bot.db.get_user_data(guild_id, user_id)
        
        # rastale sır cek
        secret = await self.bot.db.random_secret(guild_id)
        
        if not secret: return await ctx.send("📭 Kutu boş.")
        if user_data['xp'] < 100: return await ctx.send("🚫 Paran yetmiyor. 100 XP lazım.")
        
        # xp dus
        await self.bot.db.add_xp(guild_id, user_id, -100)
        
        await ctx.send(embed=discord.Embed(title="🕵️‍♂️ SIR", description=f"*\"{secret}\"*", color=discord.Color.dark_red()))

    @commands.command()
    async def itiraf(self, ctx, *, m: str):
        try: await ctx.message.delete()
        except: pass
        
        guild_id = ctx.guild.id
        
        
        settings = await self.bot.db.get_server_settings(guild_id)
        itiraf_channel_id = settings['itiraf_channel_id']
        
        if itiraf_channel_id:
            ch = self.bot.get_channel(itiraf_channel_id)
            if ch:
                await ch.send(embed=discord.Embed(title="🤫 İTİRAF", description=m, color=discord.Color.dark_grey()))
            else:
                await ctx.send("❌ İtiraf kanalı bulunamadı. Lütfen kurulumu kontrol edin.", delete_after=5)
        else: 
            await ctx.send("❌ İtiraf kanalı ayarlanmamış.", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def cekilis(self, ctx, sure: str, *, odul: str):
        s = parse_duration(sure) 
        if s == -1: return await ctx.send("Süre hatalı. Örn: `1m`, `10s`")
        
        embed = discord.Embed(title="🎉 ÇEKİLİŞ BAŞLADI!", description=f"Ödül: **{odul}**\nSüre: **{sure}**", color=discord.Color.blue())
        msg = await ctx.send(embed=embed); await msg.add_reaction("🎉")
        
        await asyncio.sleep(s)
        
        try:
            new_msg = await ctx.channel.fetch_message(msg.id)
            
            # bot olmayanlar
            users = [u async for u in new_msg.reactions[0].users() if not u.bot]
            
            if users: 
                winner = random.choice(users)
                await ctx.send(f"🏆 **TEBRİKLER!** {winner.mention}, **{odul}** kazandın!")
            else: 
                await ctx.send("Kimse katılmadı.")
        except Exception as e:
            await ctx.send(f"Çekiliş sonlandırılamadı: {e}")


async def setup(bot):
    await bot.add_cog(Sosyal(bot))
