import sqlite3
import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.all()
intents.members = True
TOKEN = 'MTAxNzA0NjExNTAwNDE5MDc1MA.GOAytn.ASoJU6qof-jYrbBYY31orrB9_83CF4_O68umFo'
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())
client.remove_command("help")


@client.event
async def on_ready():
    print("Bot is ready")

initial_extensions = []

for f in os.listdir('./cogs'):
    if f.endswith(".py"):
        initial_extensions.append(f[:-3])

print(initial_extensions)


@client.command()
async def pomoc(ctx):
    embed = discord.Embed(title="Pomoc", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                          description="Wypisuje komendy", color=0x10982b)
    embed.add_field(name="Pomoc", value="wyświetla komendy", inline=True)
    embed.add_field(name="Profile", value="Pokazuje profil twój lub kogoś", inline=True)

    await ctx.send(embed=embed)


@client.command(pass_context=True, aliases=["p"])
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    name = member.display_name
    pfp = member.display_avatar

    db = sqlite3.connect("ministranci_economy.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM ministranci_economy WHERE user_id = {member.id}")
    record = cursor.fetchone()
    cursor.close()
    db.close()

    embed = discord.Embed(title="Profil", colour=discord.Colour.blue())
    embed.set_author(name=f"{name}")
    embed.set_thumbnail(url=f"{pfp}")
    embed.add_field(name="Hajs", value=f"{record[1]} :cookie:", inline=True)
    embed.add_field(name="zarobki", value=f"{record[9]} :cookie:", inline=True)
    embed.add_field(name="Punkty ogolem", value=int(record[2]), inline=False)
    embed.add_field(name="Punkty w tym miesiacu", value=int(record[3]), inline=False)
    embed.add_field(name="Poziom - aktywność", value=int(record[4]), inline=False)
    embed.add_field(name="exp", value=int(record[5]), inline=False)

    embed.set_footer(text=f"{name} Made this Embed")
    await ctx.send(embed=embed)


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await client.start(TOKEN)


asyncio.run(main())
