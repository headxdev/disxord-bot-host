"""
Command Template: Ping
Category: Basic
Author: headx - the psychon
Description: A simple ping command that shows bot latency
"""

import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        Get the bot's current latency
        Usage: !ping
        """
        # Calculate latency
        latency = round(self.bot.latency * 1000)
        
        # Create embed with latency info
        embed = discord.Embed(
            title="🏓 Pong!",
            color=discord.Color.green() if latency < 100 else discord.Color.orange()
        )
        embed.add_field(name="Bot Latency", value=f"{latency}ms")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        # Send response
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Ping(bot))