import discord
from discord.ext import commands
import sqlite3


class BotStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, game):
        """ Zmienia status bota na *w grze*
        __.komenda nazwa__
        koszt 4 :cookie:
            """
        author = ctx.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
        cookies = cursor.fetchone()

        cookies = int(cookies[1])
        if cookies < 4:
            await ctx.send("This command cost 4 :cookie: ")
        else:
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id = ?"
            cookies -= 4
            val = (cookies, author.id)
            cursor.execute(sql, val)
            await ctx.message.delete()
            await ctx.send("status change: -4 :cookie:")
            db.commit()
            await self.bot.change_presence(activity=discord.Game(name=game))

        cursor.close()
        db.close()

    @commands.command()
    async def stream(self, ctx, *, video):
        """ Zmienia status bota na *streamuje*
        __.komenda nazwa__
        koszt 4 :cookie:
            """
        author = ctx.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
        cookies = cursor.fetchone()

        cookies = int(cookies[1])
        if cookies < 4:
            await ctx.send("This command cost 4 :cookie: ")
        else:
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id = ?"
            cookies -= 4
            val = (cookies, author.id)
            cursor.execute(sql, val)
            await ctx.message.delete()
            await ctx.send("status change: -4 :cookie:")
            db.commit()
            await self.bot.change_presence(activity=discord.Streaming(name=video,
                                                                  url="https://www.youtube.com/watch?v=K5Sy01mDvww&ab_channel=Parafia%C5%9Bw.MariiMagdalenywCieszynie"))
        cursor.close()
        db.close()


    @commands.command()
    async def listen(self, ctx, *,music):
        """ Zmienia status bota na *słucha*
        __.komenda nazwa__
        koszt 4 :cookie:
            """
        author = ctx.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
        cookies = cursor.fetchone()

        cookies = int(cookies[1])
        if cookies < 4:
            await ctx.send("This command cost 4 :cookie: ")
        else:
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id = ?"
            cookies -= 4
            val = (cookies, author.id)
            cursor.execute(sql, val)
            await ctx.message.delete()
            await ctx.send("status change: -4 :cookie:")
            db.commit()
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=music))

        cursor.close()
        db.close()

    @commands.command()
    async def watch(self, ctx, *, film):
        """ Zmienia status bota na *ogląda*
        __.komenda nazwa__
        koszt 4 :cookie:
        ------------------------------------------------------------"""
        author = ctx.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
        cookies = cursor.fetchone()

        cookies = int(cookies[1])
        if cookies < 4:
            await ctx.send("This command cost 4 :cookie: ")
        else:
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id = ?"
            cookies -= 4
            val = (cookies, author.id)
            cursor.execute(sql, val)
            await ctx.message.delete()
            await ctx.send("status change: -4 :cookie:")
            db.commit()
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=film))

        cursor.close()
        db.close()


async def setup(bot):
    await bot.add_cog(BotStatus(bot))
