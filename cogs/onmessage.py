import asyncio
import typing
import discord
from discord.ext import commands
import sqlite3
import random
import datetime


class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1, 60.0, commands.BucketType.member)  # Change accordingly
        self._cd2 = commands.CooldownMapping.from_cooldown(1, 3600.0, commands.BucketType.member)
        # rate, per, BucketType

    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    def get_ratelimit2(self, message: discord.Message) -> typing.Optional[int]:
        bucket = self._cd2.get_bucket(message)
        return bucket.update_rate_limit()


    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT user_id FROM ministranci_economy WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None and not author.bot:
            sql = ("INSERT INTO ministranci_economy"
                   "(user_id, "
                   "cookies, "
                   "points_gen, "
                   "points_month, "
                   "lvl, "
                   "exp, "
                   "luck, "
                   "mysteries, "
                   "ping, "
                   "earnings) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            x = random.randint(80, 120)
            val = (author.id, 100, 0, 0, 1, 0, x, 0, 0, 1)
            cursor.execute(sql, val)
        ratelimit = self.get_ratelimit(message)
        if ratelimit is None:
            cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
            pts = cursor.fetchone()
            x = random.randint(3, 5)
            lvl = pts[4]
            exp = pts[5]
            exp += x
            earn = int(1 + lvl / 10)
            if exp / lvl >= 25:
                exp -= lvl * 25
                lvl += 1
                await message.channel.send(f"Congrats {author.mention}, you have just reached {lvl} lvl")
                if lvl % 10 == 0:
                    await message.channel.send(f"Your income has increased by 1")
            sql = f"UPDATE ministranci_economy SET lvl = ?, exp = ?, earnings = ? WHERE user_id= ?"
            val = (lvl, exp, earn, author.id)
            cursor.execute(sql, val)
        db.commit()

        ##########################################

        ratelimit2 = self.get_ratelimit2(message)
        if ratelimit2 is None:
            cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
            pts = cursor.fetchone()
            x = pts[9]
            cookies = pts[1]
            cookies += x
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id= ?"
            val = (cookies, author.id)
            cursor.execute(sql, val)
        db.commit()

        cursor.close()
        db.close()


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
