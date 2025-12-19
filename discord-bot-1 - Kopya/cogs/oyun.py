import discord
from discord.ext import commands
import random
import asyncio
import config

class Oyun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_game_word = {} #kelime oyunu icin
    
    @commands.command()
    async def word_game(self, ctx, rounds: int = 1):
        
        guild_id = ctx.guild.id
        
        if rounds > 5: rounds = 5 
        
        await ctx.send(f" **KELİME OYUNU BAŞLIYOR!** Toplam {rounds} el oynayacağız.")
        await asyncio.sleep(2)

        for i in range(rounds):

            word = random.choice(config.KELIMELER)
            self.current_game_word[guild_id] = word
            
            #harfleri mix et
            letters = list(word)
            random.shuffle(letters)
            mixed = " ".join(letters).upper()
            
            embed = discord.Embed(title=f"EL {i+1}/{rounds}", description=f"Bu kelime ne?\n\n**{mixed}**\n\nİlk bilen 150 XP kapar!", color=discord.Color.orange())
            await ctx.send(embed=embed)
            
            def check(m):
                #burda kelimeyi bilmis mi diye kontrol ediyoruz
                return m.channel == ctx.channel and m.content.lower().strip() == word and not m.author.bot

            try:
                #30 saniye bekliyoruz
                msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                
                #kazananı odullendir
                await self.bot.db.add_xp(guild_id, msg.author.id, 150)
                await ctx.send(f" **TEBRİKLER!** {msg.author.mention} bildi! **+150 XP**")
                
            except asyncio.TimeoutError:
                await ctx.send(f"Süre doldu! Cevap: **{word.upper()}** idi.")
            
            self.current_game_word[guild_id] = None
            await asyncio.sleep(2)

        await ctx.send("Oyun bitti!")

    @commands.command()
    async def duello(self, ctx, member: discord.Member, amount: int):
        #baska bi kullanıyla düello at
        if member.id == ctx.author.id or member.bot:
            return await ctx.send(f"{config.EMOJIS['error']} Kendinle veya botla kapışamazsın.")
        if amount <= 0:
            return await ctx.send("0 xp ile kapisamazsin.")
            
        # bakiye kontrol
        user_d = await self.bot.db.get_user_data(ctx.guild.id, ctx.author.id)
        target_d = await self.bot.db.get_user_data(ctx.guild.id, member.id)

        if user_d['xp'] < amount:
            return await ctx.send("Senin paran yetmiyor!")
        if target_d['xp'] < amount:
            return await ctx.send("Rakibin parası yetmiyor!")

        await ctx.send(f"{member.mention}, {ctx.author.mention} seni **{amount} XP** bahsine düelloya çağırıyor! Kabul etmek için `kabul` yaz.")

        #kabul kontrolü
        def check(m):
            return m.author == member and m.channel == ctx.channel and m.content.lower() == "kabul"

        try:
            await self.bot.wait_for('message', check=check, timeout=30.0)
            
            #yuzde 50 sans
            winner = random.choice([ctx.author, member])
            loser = member if winner == ctx.author else ctx.author
        
            await self.bot.db.add_xp(ctx.guild.id, winner.id, amount)
            await self.bot.db.add_xp(ctx.guild.id, loser.id, -amount)
            
            await ctx.send(f"**KAZANAN:** {winner.mention}!\n**+{amount} XP** kazandı, {loser.mention} kaybetti.")

        except asyncio.TimeoutError:
            await ctx.send("Düello kabul edilmedi veya süre doldu.")

    @commands.command()
    async def yazitura(self, ctx, amount: int, choice: str):
        choice = choice.lower()
        if choice not in ['yazi', 'tura']:
            return await ctx.send("Lütfen `yazi` veya `tura` seçin.")
        if amount <= 0:
            return await ctx.send("Miktar gir.")
            
        # bakiye kontrol
        user_d = await self.bot.db.get_user_data(ctx.guild.id, ctx.author.id)
        if user_d['xp'] < amount:
             return await ctx.send("Yetersiz bakiye.")

        result = random.choice(['yazi', 'tura'])        
        if result == choice:
            await self.bot.db.add_xp(ctx.guild.id, ctx.author.id, amount)
            await ctx.send(f" **KAZANDIN!** Para **{result.upper()}** geldi. **+{amount} XP**")
        else:
            await self.bot.db.add_xp(ctx.guild.id, ctx.author.id, -amount)
            await ctx.send(f"**KAYBETTİN!** Para **{result.upper()}** geldi. **-{amount} XP**")

    #anket
    @commands.command()
    async def anket(self, ctx, *, question: str):
        embed = discord.Embed(title="ANKET", description=question, color=discord.Color.blue())
        embed.set_footer(text=f"{ctx.author.display_name} sordu.")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

async def setup(bot):
    await bot.add_cog(Oyun(bot))