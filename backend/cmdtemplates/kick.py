"""
Command Template: Kick
Category: Moderation
Author: headx - the psychon
Description: Kick a member from the server with optional reason
"""

import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        Kick a member from the server
        Usage: !kick @member [reason]
        """
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("You can't kick someone with a higher or equal role!")
        
        reason = reason or f"Kicked by {ctx.author}"
        
        # Create embed for kick notification
        embed = discord.Embed(
            title="👢 Member Kicked",
            description=f"{member.mention} has been kicked from the server.",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason", value=reason)
        embed.add_field(name="Moderator", value=ctx.author.mention)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        
        # Try to DM the kicked member
        try:
            await member.send(f"You were kicked from {ctx.guild.name}\nReason: {reason}")
        except:
            embed.set_footer(text="Could not DM member about kick")
        
        # Kick member
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Kick(bot))
