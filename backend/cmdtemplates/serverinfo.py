"""
Standard Command Template: Server Info
Category: Basic
Author: headx - the psychon
"""

import discord
from discord.ext import commands
from datetime import datetime

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx):
        """
        Show detailed information about the server
        Usage: !serverinfo
        """
        guild = ctx.guild
        
        # Collect role info
        role_count = len(guild.roles)
        roles = [role.mention for role in guild.roles[::-1][:10]] # Top 10 roles
        
        # Count channels
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        # Member counts
        total_members = guild.member_count
        online_members = len([m for m in guild.members if m.status != discord.Status.offline])
        
        # Create embed
        embed = discord.Embed(
            title=f"{guild.name} Server Information",
            description=guild.description or "No description set",
            color=guild.owner.color if guild.owner and guild.owner.color != discord.Color.default() else discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        # Set server icon as thumbnail if available
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        # Basic info
        embed.add_field(
            name="Owner",
            value=guild.owner.mention if guild.owner else "Unknown",
            inline=True
        )
        embed.add_field(
            name="Created At",
            value=discord.utils.format_dt(guild.created_at, 'R'),
            inline=True
        )
        embed.add_field(
            name="Server ID",
            value=guild.id,
            inline=True
        )
        
        # Member stats
        embed.add_field(
            name="Members",
            value=f"Total: {total_members}\nOnline: {online_members}",
            inline=True
        )
        
        # Channel stats
        embed.add_field(
            name="Channels",
            value=f"Text: {text_channels}\nVoice: {voice_channels}\nCategories: {categories}",
            inline=True
        )
        
        # Server features
        if guild.features:
            embed.add_field(
                name="Features",
                value="\n".join(f"✅ {feature.replace('_', ' ').title()}" for feature in guild.features),
                inline=False
            )
        
        # Roles (top 10 + total count)
        embed.add_field(
            name=f"Roles ({role_count})",
            value=" ".join(roles) + ("..." if role_count > 10 else ""),
            inline=False
        )
        
        # Server boost status
        if guild.premium_tier > 0:
            boost_info = (
                f"Level {guild.premium_tier}\n"
                f"Boosts: {guild.premium_subscription_count}\n"
                f"Boosters: {len(guild.premium_subscribers)}"
            )
            embed.add_field(name="Server Boost", value=boost_info, inline=True)
        
        # Additional info in footer
        embed.set_footer(
            text=f"Requested by {ctx.author} | Verification Level: {guild.verification_level}"
        )
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ServerInfo(bot))
