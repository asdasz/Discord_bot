import discord
from discord.ext import commands
#import asyncio
import sqlite3


class Raitings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rating(self, ctx):
        """ Wyświetla ranking zależny od hajsu :cookie:
        __.komenda__
            """
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        sql = "SELECT * FROM ministranci_economy ORDER BY cookies DESC"
        cursor.execute(sql)
        records = cursor.fetchall()
        embed = discord.Embed(title="Ranking", colour=discord.Colour.blue())
        k = 1
        for i in records:
            embed.add_field(name=k, value=f"<@{i[0]}> has {i[1]} :cookie:", inline=False)
            k += 1
        cursor.close()
        db.commit()
        db.close()
        await ctx.send(embed=embed)

    @commands.command()
    async def points(self, ctx):
        """ Wyświetla ranking punktów ogółem
        __.komenda__
            """
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        sql = "SELECT * FROM ministranci_economy ORDER BY points_gen DESC"
        cursor.execute(sql)
        records = cursor.fetchall()
        embed = discord.Embed(title="Ranking", colour=discord.Colour.blue())
        k = 1
        for i in records:
            embed.add_field(name=k, value=f"<@{i[0]}> has {i[2]} points in general", inline=False)
            k += 1
        cursor.close()
        db.commit()
        db.close()
        await ctx.send(embed=embed)


    @commands.command()
    async def month(self, ctx):
        """ Wyświetla ranking punktów w bierzącym miesiącu
        __.komenda__
            """
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        sql = "SELECT * FROM ministranci_economy ORDER BY points_month DESC"
        cursor.execute(sql)
        records = cursor.fetchall()
        embed = discord.Embed(title="Ranking", colour=discord.Colour.blue())
        k = 1
        for i in records:
            embed.add_field(name=k, value=f"<@{i[0]}> has collected {i[3]} points during this month", inline=False)
            k += 1
        cursor.close()
        db.commit()
        db.close()
        await ctx.send(embed=embed)

    @commands.command()
    async def level(self, ctx):
        """ Wyświetla ranking aktywności
        __.komenda__
        ------------------------------------------------------------"""
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        sql = "SELECT * FROM ministranci_economy ORDER BY lvl DESC"
        cursor.execute(sql)
        records = cursor.fetchall()
        embed = discord.Embed(title="Ranking", colour=discord.Colour.blue())
        k = 1
        for i in records:
            embed.add_field(name=k, value=f"<@{i[0]}> has  {i[4]} level", inline=False)
            k += 1
        cursor.close()
        db.commit()
        db.close()
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Raitings(bot))
