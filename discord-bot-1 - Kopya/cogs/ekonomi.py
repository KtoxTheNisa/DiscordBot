import config
import discord
from discord.ext import commands
import asyncio
import random
import time



class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #ekonomi    
    @commands.command()
    async def borsa(self, ctx):
        guild_id, user_id = ctx.guild.id, ctx.author.id
        
        #botcoin fiyatını cekiyoruz
        price = await self.bot.db.get_botcoin()
        user_data = await self.bot.db.get_user_data(guild_id, user_id)
        
        user_xp = user_data['xp']
        user_bc = user_data['botcoin']

        embed = discord.Embed(title="📈 BotCoin Borsası", color=config.COLORS.get('Gold', discord.Color.gold()))
        embed.add_field(name="BotCoin Fiyatı", value=f"**{price} XP**")
        embed.add_field(name="Cüzdanınız", value=f"💰 {user_xp} XP\n{config.EMOJIS.get('coin', '🪙')} {user_bc} BC")
        await ctx.send(embed=embed)

    @commands.command()
    async def buy_coin(self, ctx, n: int):
        if n <= 0: return await ctx.send("Geçersiz miktar.")
        
        guild_id, user_id = ctx.guild.id, ctx.author.id
        
        #botcoin fiyatını cekiyoruz yine
        price = await self.bot.db.get_botcoin()
        cost = price * n
        
        user_data = await self.bot.db.get_user_data(guild_id, user_id)
        
        if user_data['xp'] < cost: 
            return await ctx.send(f"{config.EMOJIS.get('error', '❌')} Yetersiz XP. {cost} XP lazım.")
        
        await self.bot.db.add_xp(guild_id, user_id, -cost) #xp düstü
        await self.bot.db.add_coin(guild_id, user_id, n) #coin alındı
        
        await ctx.send(f"{config.EMOJIS.get('success', '✅')} **{n} BotCoin** alındı. {cost} XP ödendi.")

    @commands.command()
    async def sell_coin(self, ctx, n: int):
        if n <= 0: return await ctx.send("Geçersiz miktar.")
        
        guild_id, user_id = ctx.guild.id, ctx.author.id
        
        price = await self.bot.db.get_botcoin()
        earned = price * n
        
        user_data = await self.bot.db.get_user_data(guild_id, user_id)
        
        if user_data['botcoin'] < n: 
            return await ctx.send(f"{config.EMOJIS.get('error', '❌')} Yetersiz Botcoin.")
        
        await self.bot.db.add_coin(guild_id, user_id, -n) # coin düştük
        await self.bot.db.add_xp(guild_id, user_id, earned) # xp ekledik
        
        await ctx.send(f"{config.EMOJIS.get('success', '✅')} **{n} BotCoin** sattın. {earned} XP kazandın.")

    #daily icin fonksiyon
    @commands.command()
    async def daily(self, ctx):
        guild_id, user_id = ctx.guild.id, ctx.author.id
        
        user_data = await self.bot.db.get_user_data(guild_id, user_id)
        last_daily = user_data['last_daily']

        wait_time = 24*60*60 #24 saat
        now = int(time.time())
        #daily kontrolü yapılıyor
        if now - last_daily > wait_time:
            daily_xp = 200
            
            await self.bot.db.claim_daily(guild_id, user_id, daily_xp)
            
            await ctx.send(f"💰 **{daily_xp} günlük XP alındı.")
        else: 
            left = wait_time - (now - last_daily)
            hours = int(left / 3600)
            minutes = int((left % 3600) / 60)
            
            if hours > 0:
                time_left = f"**{hours} saat** ve **{minutes} dakika**"
            else:
                time_left = f"**{minutes} dakika**"
                
            await ctx.send(f"{config.EMOJIS.get('error', '⏳')} Günlük ödül bekleniyor. {time_left} bekleme süresi.")

    #steal icin fonksiyon
    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def steal(self, ctx):
        guild_id, user_id = ctx.guild.id, ctx.author.id
        
        luck = random.randint(1, 100)
        
        if luck <= 20: #kazanma sansını bilerek düsük tutuyorum
            win_amount = random.randint(200, 600)
            await self.bot.db.add_xp(guild_id, user_id, win_amount)
            embed = discord.Embed(title="💰 VURGUN!", description=f"**+{win_amount} XP**", color=config.COLORS.get('Success', discord.Color.green()))
            embed.set_image(url="https://media.tenor.com/images/0e30f323232433765700d367e19c5622/tenor.gif")
            
        elif luck <= 60: 
            lost_amount = random.randint(100, 300)
            await self.bot.db.add_xp(guild_id, user_id, -lost_amount)
            embed = discord.Embed(title="🚔 YAKALANDIN!", description=f"**-{lost_amount} XP**", color=config.COLORS.get('Error', discord.Color.red()))
            embed.set_image(url="https://media.tenor.com/images/2b7c76d9556035c2e66227b267950223/tenor.gif")
            
        else: #kalan 20 sanla bir sey olmuyor
            embed = discord.Embed(title="🏃‍♂️ KAÇTIN!", description="0 XP kazandın", color=discord.Color.orange())
            
        await ctx.send(embed=embed)
        
    @steal.error
    async def steal_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown): 
            await ctx.send(f"{config.EMOJIS.get('error', '⏳')} soygun için **{int(error.retry_after)} saniye** daha beklemen lazım.")

    @commands.command()
    async def market(self, ctx): 
        #burasi gelistirilebilir simdilik boyle
        await ctx.send(embed=discord.Embed(title="🛒 MARKET", description="1. Zengin Rozeti (1000 XP)\n satın alındı.", color=config.COLORS.get('Success', discord.Color.green())))
        
    @commands.command()
    async def buy(self, ctx, item_id: int):
        guild_id, user_id = ctx.guild.id, ctx.author.id
        user_data = await self.bot.db.get_user_data(guild_id, user_id)
        
        if item_id == 1:
            cost = 1000
            if user_data['xp'] < cost: 
                return await ctx.send(f"{config.EMOJIS.get('error!', '❌')} paran yetmiyor. {cost} XP lazım.")
            
            await self.bot.db.add_xp(guild_id, user_id, -cost)
            
            await ctx.send(f"{config.EMOJIS.get('success', '✅')} **Zengin Rozeti** aldın!")
        else: 
            await ctx.send("Öyle bir ürün bulunmamaktadır.")


async def setup(bot):
    await bot.add_cog(Economy(bot))
