import discord
from discord.ext import commands
import asyncio


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time):
        """ Wycisza użytkownika na określony czas (tylko dla adminów)
        __.komenda <@user> liczba__
            """
        role = discord.utils.get(ctx.guild.roles, name='muted')
        await member.add_roles(role)
        print(f"{member.nick} was muted for {int(time)} s")
        await ctx.send(f"{member.mention} was muted for {int(time)} s")
        await asyncio.sleep(int(time))
        await member.remove_roles(role)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """ Odcisza użytkownika (tylko dla adminów)
        __.komenda <@user>__
            """
        role = discord.utils.get(ctx.guild.roles, name='muted')
        await ctx.send(f"{member.mention} was unmuted")
        await member.remove_roles(role)

    @commands.command()
    @commands.is_owner()
    async def kill(self, ctx):
        """ Wyłącza bota, tylko dla JW
        __.komenda__
        ------------------------------------------------------------"""
        await ctx.send(f'Byeee :-(')
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(Moderation(bot))
