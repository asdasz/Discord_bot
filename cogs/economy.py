import discord
from discord.ext import commands
import asyncio
import sqlite3


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def correct(self, ctx, member: discord.Member, amount):
        """ Osoba tworząca zadania przyznaje :cookie: za ich rozwiązanie
        __.komenda <@user> liczba__
            """
        amount = int(amount)
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {member.id}")
        pts = cursor.fetchone()
        print(pts)
        exp = pts[5]
        exp += int(amount) * 2
        cookies = pts[1]
        cookies += int(amount)
        print(cookies)

        sql = f"UPDATE ministranci_economy SET cookies = ?, exp = ? WHERE user_id= ?"
        val = (cookies, exp, member.id)
        cursor.execute(sql, val)

        cursor.close()
        db.commit()
        db.close()
        await ctx.send(f"{member.mention} added  {amount} :cookie: and {amount*2} exp")

    @commands.command()
    async def givecookies(self, ctx, member: discord.Member, amount):
        """ przekazuje :cookie: innemu użytkownikowi
        __.komenda <@user> liczba__
        ------------------------------------------------------------"""
        author = ctx.author
        amount = int(amount)
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
        pts = cursor.fetchone()
        cookies = int(pts[1])
        if cookies < amount:
            await ctx.send(f"you don't have enough :cookie: ")
        else:
            cookies -= amount
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id= ?"
            val = (cookies, author.id)
            cursor.execute(sql, val)
            cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {member.id}")
            pts2 = cursor.fetchone()
            cookies2 = int(pts2[1])
            cookies2 += amount
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id= ?"
            val = (cookies2, member.id)
            cursor.execute(sql, val)

            await ctx.send(f"{author.mention} send {member.mention} {amount} :cookie:")

        cursor.close()
        db.commit()
        db.close()


async def setup(bot):
    await bot.add_cog(Economy(bot))
