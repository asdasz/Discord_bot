import asyncio
from discord.ext import commands
import sqlite3
import random
import datetime
from discord.ext import tasks


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        #await channel.send(f"{member.mention} Witaj na serwerze")


        await member.send(f"```Cześć, jestem głównym botem na tym serwerze!\n\
       Staram się dbać o porządek, liczyć punkty, ale także umożliwiam rozrywkę np. w postaci hazardu :)) \n\
       Jakby ktoś cię kiedyś wyrzucił (przypadkowo bądź celowo) tu masz link powrotny, miłej zabawy!```\n\
       https://discord.gg/fU5Vksn7x5")
        print("XD")

        await member.add_roles(member.guild.get_role(817775319418273824))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        await channel.send(f" Papa {member.mention}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions required for this command.")
            return

    @commands.Cog.listener()
    async def on_midnight(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        print(current_time)

    async def updatesql(self):
        while True:
            now = datetime.datetime.now()
            then = now.replace(hour=23, minute=59, second=59)
            wait_time = (then-now).total_seconds()
            print(now)
            print(wait_time)
            await asyncio.sleep(wait_time)


    @commands.Cog.listener()
    async def on_ready(self):
        #tworzenie bd
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS ministranci_economy(
            user_id INT, 
            cookies INT, 
            points_gen INT, 
            points_month INT, 
            lvl INT, 
            exp INT, 
            luck INT, 
            mysteries INT, 
            ping INT,
            earnings INT)''')
        print("Online")
        #await self.updatesql()





async def setup(bot):
    await bot.add_cog(Events(bot))
