import discord
from discord.ext import commands
import time
import config

class Yonetim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setting(self, ctx, channel: discord.TextChannel):
        #log kanalı seyi
        await self.bot.db.set_log_channel(ctx.guild.id, channel.id)
        await ctx.send(f"{config.EMOJIS['success']} Log kanalı ayarlandı: {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    #ingiliizcesini unuttum mlsf
    async def set_itirad(self, ctx, channel: discord.TextChannel):
        #itiraf kanalı seyi
        await self.bot.db.set_itiraf_channel(ctx.guild.id, channel.id)
        await ctx.send(f"{config.EMOJIS['success']} İtiraf kanalı ayarlandı: {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_trivia(self, ctx, channel: discord.TextChannel):
        
        #triva kanalo 
        await self.bot.db.set_trivia_channel(ctx.guild.id, channel.id)
        await ctx.send(f"{config.EMOJIS['success']} Trivia kanalı ayarlandı: {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def auto_role(self, ctx, role: discord.Role):
        #otorol
        await self.bot.db.set_autorole(ctx.guild.id, role.id)

        await ctx.send(f"{config.EMOJIS['success']} Otorol ayarlandı: **{role.name}**")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def tagayarla(self, ctx, tag: str):
       #bu da sunucu tagı ayarlama
        await self.bot.db.set_tag(ctx.guild.id, tag)
        await ctx.send(f"{config.EMOJIS['success']} Sunucu tagı ayarlandı: `{tag}`")

   

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
        if member.id == ctx.guild.owner_id:
            await ctx.send(f"{config.EMOJIS['error']} Sunucu sahibini atamazsın.")
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.send(f"{config.EMOJIS['error']} Bu kişinin yetkisi senden yüksek veya eşit.")
            return
            
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} sunucudan atıldı. Sebep: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
        if member.id == ctx.guild.owner_id:
            await ctx.send(f"{config.EMOJIS['error']} Sunucu sahibini yasaklayamazsın.")
            return
            
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} yasaklandı. Sebep: {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, amount: int):
        #mesaj silme seyi 
        if amount < 1:
            return await ctx.send("En az 1 mesaj silmelisin.")
        
        deleted = await ctx.channel.purge(limit=amount + 1) #+1 komut mesajı için

        await ctx.send(f"🧹 **{len(deleted)-1}** mesaj temizlendi.", delete_after=5)

    @commands.command()
    async def afk(self, ctx, *, reason="Sebep yok"):
        #afk seyis
        await self.bot.db.set_afk(ctx.guild.id, ctx.author.id, reason)
        await ctx.send(f"{ctx.author.mention} artık AFK. Sebep: {reason}")



    @commands.command(aliases=['loca'])
    async def private_channel(self, ctx, isim: str, members: commands.Greedy[discord.Member] = None):
        
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False),
            ctx.author: discord.PermissionOverwrite(connect=True)
        }
        if members:
            for m in members:
                overwrites[m] = discord.PermissionOverwrite(connect=True)
        
        #channeli olusturur
        category = ctx.channel.category
        channel = await ctx.guild.create_voice_channel(name=isim, category=category, overwrites=overwrites)
        
        #gecici kayıt
        await self.bot.db.make_tempChannel(channel.id, ctx.author.id, ctx.guild.id)
        
        await ctx.send(f"{config.EMOJIS['success']} Özel oda açıldı: {channel.mention} (48 saat sonra silinecek)")

    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_auto_role(self, ctx, channel: discord.TextChannel):
        #rol paneli
        await ctx.send(f"⏳ Paneller **{channel.mention}** kanalına kuruluyor...")

        #bunun icin fonks
        async def make_panel(baslik, veri, renk, aciklama):
            desc = f"{aciklama}\n\n"
            for emoji, isim in veri.items():
                desc += f"{emoji} ➔ **{isim}**\n"
            
            embed = discord.Embed(title=baslik, description=desc, color=renk)
            embed.set_footer(text="Rolü almak için aşağıdaki butona tıkla!")
            msg = await channel.send(embed=embed)
            
            #rol ekleme
            for emoji, isim in veri.items():
                role = discord.utils.get(ctx.guild.roles, name=isim)
                if not role:
                    #rol almadıysa
                    role_color = config.COLORS.get(isim, discord.Color.default())
                    try:
                        role = await ctx.guild.create_role(name=isim, color=role_color, reason="Otorol Kurulumu")
                    except:
                        continue 
                
                try: await msg.add_reaction(emoji)
                except: pass
                
                await self.bot.db.add_reaction_role(ctx.guild.id, msg.id, str(emoji), role.id)

        #configden cekiyoruz da config ayarlancak unutmayalım
        await make_panel("🔮 BURCUNU SEÇ", config.BURCLAR, discord.Color.purple(), "Aşağıdan burcunu seçebilirsin:")
        await make_panel("🎨 RENGİNİ SEÇ", config.RENKLER, discord.Color.gold(), "İsminin rengini seçmek için tıkla:")
        await make_panel("🎮 OYUNLAR", config.OYUNLAR, discord.Color.red(), "Oynadığın oyunları seç:")
        
        await ctx.send("Kurulum tamamlandı!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_button(self, ctx, msg_id: int, emoji: str, role: discord.Role):
        

        try:

            msg = await ctx.channel.fetch_message(msg_id)
        except:
            await ctx.send("Mesaj bulunamadı.")
            return

        try:
            await msg.add_reaction(emoji)

            await self.bot.db.add_reaction_role(ctx.guild.id, msg.id, str(emoji), role.id)
            await ctx.send(f"Buton eklendi: {emoji} -> {role.name}")
        except Exception as e:
            await ctx.send(f"Hata oluştu: {e}")

    @commands.command()
    @commands.is_owner()
    async def add_license(self, ctx, server_id: int, owner_id: int = None):
        #lisans ekleme böylerliklle manuel olarak eklemeyeceğiz bot komutu ile eklenecek
        if owner_id is None:
            owner_id = ctx.author.id 
            
        await self.bot.db.add_allowed_server(server_id, owner_id)
        await ctx.send(f"{config.EMOJIS.get('success', '✅')} Lisans eklendi! Server ID: `{server_id}`, Sahip ID: `{owner_id}`")

    @commands.command()
    @commands.is_owner()
    async def remove_license(self, ctx, server_id: int, owner_id: int = None):
        #lisans kaldırma
        if owner_id is None:
             owner_id = ctx.author.id
             
        await self.bot.db.no_money_no_bot(server_id, owner_id)
        await ctx.send(f"{config.EMOJIS.get('error', '❌')} Lisans kaldırıldı. Server ID: `{server_id}`")

async def setup(bot):
    await bot.add_cog(Yonetim(bot))