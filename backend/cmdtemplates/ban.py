"""
Command Template: Ban
Category: Moderation
Author: headx - the psychon
Description: Ban a member from the server with optional reason and delete message history
"""

import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, days: int = 0, *, reason=None):
        """
        Ban a member from the server
        Usage: !ban @member [days] [reason]
        days: Number of days of message history to delete (0-7)
        """
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("You can't ban someone with a higher or equal role!")
        
        # Validate days parameter
        days = max(0, min(7, days))  # Clamp between 0 and 7
        reason = reason or f"Banned by {ctx.author}"
        
        # Create embed for ban notification
        embed = discord.Embed(
            title="🔨 Member Banned",
            description=f"{member.mention} has been banned from the server.",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Reason", value=reason)
        embed.add_field(name="Moderator", value=ctx.author.mention)
        embed.add_field(name="Message History Deleted", value=f"{days} days")
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        
        # Try to DM the banned member
        try:
            await member.send(f"You were banned from {ctx.guild.name}\nReason: {reason}")
        except:
            embed.set_footer(text="Could not DM member about ban")
        
        # Ban member
        await member.ban(reason=reason, delete_message_days=days)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Ban(bot))
