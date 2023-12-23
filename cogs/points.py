import discord
from discord.ext import commands
#import asyncio
import sqlite3


class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def setpoints(self, ctx, member: discord.Member, amount):
        """ Nadaje użytkownikowi liczbę punktów (komenda tylko dla JW)
        __.komenda <@user> liczba__
            """
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT points_gen FROM ministranci_economy WHERE user_id = {member.id}")
        sql = f"UPDATE ministranci_economy SET points_gen = ? WHERE user_id= ?"
        val = (amount, member.id)
        print(val)
        cursor.execute(sql, val)
        cursor.close()
        db.commit()
        db.close()
        await ctx.send(f"{member.mention} points was set to {amount}")

    @commands.command()
    @commands.is_owner()
    async def setcookies(self, ctx, member: discord.Member, amount):
        """ Nadaje użytkownikowi liczbę :cookie: (komenda tylko dla JW)
        __.komenda <@user> liczba__
            """
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT cookies FROM ministranci_economy WHERE user_id = {member.id}")
        sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id= ?"
        val = (amount, member.id)
        print(val)
        cursor.execute(sql, val)
        cursor.close()
        db.commit()
        db.close()
        await ctx.send(f"{member.mention} cookies was set to {amount}")

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def addpoints(self, ctx, member: discord.Member = None, amount=5):
        """ dodaje punkty za obecność na mszy/zbiórce itp
        __.komenda <@user> (domyślnie osoba używająca komedy) liczba(domyślnie 5)__
            """
        if member == None:
            member = ctx.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT points_month FROM ministranci_economy WHERE user_id = {member.id}")
        pts = cursor.fetchone()
        pts = pts[0]
        suma = int(pts+amount)
        sql = f"UPDATE ministranci_economy SET points_month = ? WHERE user_id= ?"
        val = (suma, member.id)
        cursor.execute(sql, val)
        cursor.close()
        db.commit()
        db.close()
        await ctx.send(f"added {member.mention} {amount} points ")

    @commands.command()
    @commands.is_owner()
    async def addcookies(self, ctx, member: discord.Member = None, amount=5):
        """ dodaje :cookie:
        __.komenda <@user> liczba__
            """
        if member == None:
            member = ctx.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {member.id}")
        pts = cursor.fetchone()
        pts = pts[1]
        suma = int(pts+amount)
        sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id= ?"
        val = (suma, member.id)
        cursor.execute(sql, val)
        cursor.close()
        db.commit()
        db.close()
        await ctx.send(f"added {member.mention} {amount} :cookie: ")


    @commands.command()
    @commands.is_owner()
    async def updatemonth(self, ctx):
        """ Aktualizuje punkty na koniec miesiąca - dostęp tylko dla księdza i JW
        __.komenda__
        ------------------------------------------------------------"""
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM ministranci_economy")
        records = cursor.fetchall()

        for i in records:
            pg = i[2]
            pm = i[3]
            id = i[0]
            print(pg)
            print(pm)
            pg += pm
            pm = 0
            print(pg)
            print(pm)
            sql = f"UPDATE ministranci_economy SET points_month = ?, points_gen = ? WHERE user_id = ?"
            val = (pm, pg, id)
            cursor.execute(sql, val)

        cursor.close()
        db.commit()
        db.close()
        await ctx.send(f"updated monthly points")


async def setup(bot):
    await bot.add_cog(Points(bot))
