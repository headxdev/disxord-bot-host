"""
Command Template: Clear
Category: Moderation
Author: headx - the psychon
Description: Clear a specified number of messages from a channel
"""

import discord
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", aliases=["purge", "clean"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """
        Clear messages from the channel
        Usage: !clear [amount]
        amount: Number of messages to delete (default: 5, max: 100)
        """
        if amount < 1:
            return await ctx.send("Please specify a positive number of messages to delete!")
        
        amount = min(100, amount)  # Cap at 100 messages
        
        # Delete messages
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 for command message
        
        # Send confirmation
        confirm = await ctx.send(
            embed=discord.Embed(
                title="🧹 Channel Cleaned",
                description=f"Deleted {len(deleted)-1} messages",
                color=discord.Color.green()
            )
        )
        
        # Delete confirmation after 5 seconds
        await confirm.delete(delay=5)

def setup(bot):
    bot.add_cog(Clear(bot))
