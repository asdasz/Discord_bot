import discord
from discord.ext import commands
import sqlite3
from discord import Webhook
import aiohttp
import asyncio

class Troll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spam(self, ctx, member: discord.Member):
        """ Spamuje wiadomościami użytkownikowi
        __.komenda <@user>__
        koszt: 10 :cookie:
            """
        price = 10
        author = ctx.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
        cookies = cursor.fetchone()

        cookies = int(cookies[1])
        if cookies < price:
            await ctx.send(f"This command cost {price} :cookie: ")
        else:
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id = ?"
            cookies -= price
            val = (cookies, author.id)
            cursor.execute(sql, val)
            await ctx.message.delete()
            await ctx.send(f"spam -{price} :cookie:")
            db.commit()
            for i in range(0, 20):
                await member.send(f"spam")
                await member.send(f"You have been spammed")
                await member.send(f"LMFAO")

        cursor.close()
        db.close()

    @commands.command()
    async def poke(self, ctx, member: discord.Member):
        """ Poke'uje innego użytkownika
        __.komenda <@user>__
        koszt: 1 :cookie:
            """
        price = 1
        author = ctx.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
        cookies = cursor.fetchone()

        cookies = int(cookies[1])
        if cookies < price:
            await ctx.send(f"This command cost {price} :cookie: ")
        else:
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id = ?"
            cookies -= price
            val = (cookies, author.id)
            cursor.execute(sql, val)
            await ctx.message.delete()
            await ctx.send(f"poke -{price} :cookie:")
            db.commit()
            await member.send(f"You have been poked")

        cursor.close()
        db.close()

    @commands.command()
    async def changenick(self, ctx, member: discord.Member, *, newnick):
        """ Zmienia czyjś nick
        __.komenda <@user> NowyNick__
        koszt: 5 :cookie:
            """
        price = 5
        author = ctx.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
        cookies = cursor.fetchone()

        cookies = int(cookies[1])
        if cookies < price:
            await ctx.send(f"This command cost {price} :cookie: ")
        else:
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id = ?"
            cookies -= price
            val = (cookies, author.id)
            cursor.execute(sql, val)
            await ctx.message.delete()
            await ctx.send(f"nickname change: -{price} :cookie:")
            db.commit()
            await member.edit(nick=str(newnick))

        cursor.close()
        db.close()

    @commands.command()
    async def say(self, ctx, member: discord.Member, *, text):
        """ Sprawia że ktoś mówi coś
        __.komenda <@user> tekst__
        koszt: 5 :cookie:
            """
        price = 5
        author = ctx.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
        cookie = cursor.fetchone()
        iidd = int(cookie[0])
        cookies = int(cookie[1])
        if cookies < price:
            await ctx.send(f"This command cost {price} :cookie: ")
        else:
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id = ?"
            cookies -= price
            val = (cookies, author.id)
            cursor.execute(sql, val)
            await ctx.message.delete()
            db.commit()
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url('https://discord.com/api/webhooks/1037713494549741671/0Bb6hOFy7TVeaZd9fdlWD1vW8vaC2mmqSBGKpvaMj727ENL5Hz_5yb39MLzK3YQll36k', session=session)
                await webhook.send(text, username=member.nick, avatar_url=member.avatar.url)

        cursor.close()
        db.close()

    @commands.command()
    async def shutup(self, ctx, member: discord.Member):
        """ Wycisza kogoś na 3 minuty
        __.komenda <@user>__
        koszt: 8 :cookie:
        ------------------------------------------------------------"""
        price = 8
        author = ctx.author
        db = sqlite3.connect("ministranci_economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {author.id}")
        cookie = cursor.fetchone()
        iidd = int(cookie[0])
        cookies = int(cookie[1])
        role = discord.utils.get(ctx.guild.roles, name='muted')
        if cookies < price:
            await ctx.send(f"This command cost {price} :cookie: ")
        else:
            sql = f"UPDATE ministranci_economy SET cookies = ? WHERE user_id = ?"
            cookies -= price
            val = (cookies, author.id)
            cursor.execute(sql, val)
            await ctx.message.delete()
            db.commit()
            await member.add_roles(role)
            await asyncio.sleep(10)
            await member.remove_roles(role)

        cursor.close()
        db.close()


async def setup(bot):
    await bot.add_cog(Troll(bot))
