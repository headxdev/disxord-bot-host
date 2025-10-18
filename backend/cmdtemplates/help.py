"""
Standard Command Template: Help Command
Category: Basic
Author: headx - the psychon
"""

import discord
from discord.ext import commands
from typing import Optional

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = None

    def cog_unload(self):
        """Reset the help command when the cog is unloaded"""
        self.bot.help_command = self._original_help_command

    @commands.command(name="help")
    async def help(self, ctx, command_name: Optional[str] = None):
        """
        Show help for all commands or specific command
        Usage: !help [command]
        """
        if command_name:
            # Show help for specific command
            cmd = self.bot.get_command(command_name)
            if not cmd:
                return await ctx.send(f"Command `{command_name}` not found!")

            embed = discord.Embed(
                title=f"Help: {cmd.name}",
                description=cmd.help or "No description available",
                color=discord.Color.blue()
            )
            
            if cmd.aliases:
                embed.add_field(
                    name="Aliases",
                    value=", ".join(cmd.aliases),
                    inline=False
                )

            usage = f"{ctx.prefix}{cmd.name}"
            if cmd.signature:
                usage += f" {cmd.signature}"
            embed.add_field(name="Usage", value=f"`{usage}`", inline=False)

        else:
            # Show all commands grouped by cog
            embed = discord.Embed(
                title="Bot Commands",
                description="Use `!help <command>` for detailed information",
                color=discord.Color.blue()
            )

            # Group commands by cog
            for cog_name, cog in self.bot.cogs.items():
                # Skip if cog has no commands or all are hidden
                visible_commands = [c for c in cog.get_commands() if not c.hidden]
                if not visible_commands:
                    continue

                # Add field for each cog
                command_list = []
                for cmd in visible_commands:
                    command_list.append(f"`{cmd.name}`")
                
                if command_list:
                    embed.add_field(
                        name=cog_name,
                        value=" ".join(command_list),
                        inline=False
                    )

        # Add footer with bot info
        embed.set_footer(
            text=f"Made by headx - the psychon | Type {ctx.prefix}help <command> for details"
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
