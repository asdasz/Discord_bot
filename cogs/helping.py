# import cmd
# from typing import Optional
# import discord
# from discord.ext import commands
#
# class Help_command(commands.MinimalHelpCommand):
#     def get_command_signature(self, command):
#         return "{0.clean_prefix}{1.qualifier_name} {1.signature}".format(self, command)
#
#     async def help_embed(self, title: str, description: Optional[str] = None, mapping: Optional[str] = None):
#         embed = discord.Embed(title=title)
#         if description:
#             embed.description = description
#         if mapping:
#             for cog, commands_set in mapping.items():
#                 filtered = await self.filter_commands(commands_set, sort=True)
#                 if not filtered:
#                     continue
#                 name = cog.qualified_name if cog else "No category"
#                 cmd_list = "\u2002".join(f"`{self.context.clean_prefix}{cmd.name}`" for cmd in filtered)
#                 value = (f"{cog.description}\n{cmd_list}:") if cog and cog.description else cmd_list)
#                 embed.add_field(name = name, value=value)
#         return embed
#
#     async def send_bot_help(self, mapping: dict):
#         embed = await self.help_embed(title="Bot commands", description=self.context.bot.description, mapping=mapping)
#         await self.get_destination().send(embed=embed)
#
#     async def send_command_help(self, command: commands.Command):
#         pass
#
#     async def send_cog_help(self, cog: commands.Cog):
#         pass
#
#
# class HelpCog(commands.Cog, name="help"):
#     def __init__(self, bot):
#         self.original_help_command = bot.help_command
#         bot.help_command = Help_command()
#         bot.help_command.cog = self
#
#     def cog_unload(self):
#         self.bot.help_command = self.original_help_command
#
#
# async def setup(bot: commands.Bot):
#     await bot.add_cog(HelpCog(bot))



import discord
from discord.ext import commands


class Help(commands.Cog):
    """ Help commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *commands: str):
        """ Shows this message """
        bot = ctx.bot
        embed = discord.Embed(title="Help", description="List of all commands")

        def generate_usage(command_name):
            """ Generates a string of how to use a command """
            temp = f'.'
            command = bot.get_command(command_name)
            # Aliases
            if len(command.aliases) == 0:
                temp += f'{command_name}'
            elif len(command.aliases) == 1:
                temp += f'[{command.name}|{command.aliases[0]}]'
            else:
                t = '|'.join(command.aliases)
                temp += f'[{command.name}|{t}]'
            # Parameters
            params = f' '
            for param in command.clean_params:
                params += f'<{command.clean_params[param]}> '
            temp += f'{params}'
            return temp

        def generate_command_list(cog):
            """ Generates the command list with properly spaced help messages """
            # Determine longest word
            max = 0
            for command in bot.get_cog(cog).get_commands():
                if not command.hidden:
                    if len(f'{command}') > max:
                        max = len(f'{command}')
            #Build list
            temp = ""
            for command in bot.get_cog(cog).get_commands():
                if command.hidden:
                    temp += ''
                elif command.help is None:
                    temp += f'{command}\n'
                else:
                    temp += f'`{command}`'
                    for i in range(0, max - len(f'{command}') + 1):
                        temp += '   '
                    temp += f'{command.help}\n'
            return temp

        # Help by itself just lists our own commands.
        if len(commands) == 0:
            for cog in bot.cogs:
                temp = generate_command_list(cog)
                if temp != "":
                    embed.add_field(name=f'**{cog}**', value=temp, inline=False)
        elif len(commands) == 1:
            # Try to see if it is a cog name
            name = commands[0].capitalize()
            command = None

            if name in bot.cogs:
                cog = bot.get_cog(name)
                msg = generate_command_list(name)
                embed.add_field(name=name, value=msg, inline=False)
                msg = f'{cog.description}\n'
                embed.set_footer(text=msg)

            # Must be a command then
            else:
                command = bot.get_command(name)
                if command is not None:
                    help = f''
                    if command.help is not None:
                        help = command.help
                    embed.add_field(name=f'**{command}**',
                                    value=f'{command.description}```{generate_usage(name)}```\n{help}',
                                    inline=False)
                else:
                    msg = ' '.join(commands)
                    embed.add_field(name="Not found", value=f'Command/category `{msg}` not found.')
        else:
            msg = ' '.join(commands)
            embed.add_field(name="Not found", value=f'Command/category `{msg}` not found.')

        await ctx.send(embed=embed)
        return


# Cog setup
async def setup(bot):
    await bot.add_cog(Help(bot))
