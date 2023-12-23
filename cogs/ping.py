from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"{round(error.retry_after, 2)} seconds left", delete_after=5)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):
        """ Będzie służyć do hazardu
        __.komenda__
        ------------------------------------------------------------"""
        await ctx.send("Pong")


async def setup(bot):
    await bot.add_cog(Ping(bot))
