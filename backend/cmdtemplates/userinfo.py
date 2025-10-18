"""
Standard Command Template: User Info
Category: Basic
Author: headx - the psychon
"""

import discord
from discord.ext import commands
from datetime import datetime
from typing import Optional

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo")
    async def userinfo(self, ctx, member: Optional[discord.Member] = None):
        """
        Show detailed information about a user
        Usage: !userinfo [@user]
        """
        # If no member specified, use command author
        member = member or ctx.author
        
        # Create embed
        embed = discord.Embed(
            title=f"User Information - {member.name}",
            color=member.color if member.color != discord.Color.default() else discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        # Set user avatar
        embed.set_thumbnail(url=member.display_avatar.url)
        
        # Basic info
        embed.add_field(
            name="User Info",
            value=f"**Name:** {member.name}\n"
                  f"**Display Name:** {member.display_name}\n"
                  f"**ID:** {member.id}\n"
                  f"**Bot:** {'Yes' if member.bot else 'No'}\n"
                  f"**Created:** {discord.utils.format_dt(member.created_at, 'R')}",
            inline=False
        )
        
        # Server-specific info
        embed.add_field(
            name="Member Info",
            value=f"**Joined:** {discord.utils.format_dt(member.joined_at, 'R')}\n"
                  f"**Join Position:** {sorted(ctx.guild.members, key=lambda m: m.joined_at or datetime.max).index(member) + 1}\n"
                  f"**Top Role:** {member.top_role.mention if member.top_role != ctx.guild.default_role else 'None'}",
            inline=False
        )
        
        # Status and activity
        status_emojis = {
            discord.Status.online: "🟢",
            discord.Status.idle: "🟡",
            discord.Status.dnd: "🔴",
            discord.Status.offline: "⚫"
        }
        
        activities = []
        for activity in member.activities:
            if isinstance(activity, discord.Game):
                activities.append(f"Playing {activity.name}")
            elif isinstance(activity, discord.Streaming):
                activities.append(f"Streaming {activity.name}")
            elif isinstance(activity, discord.Spotify):
                activities.append(f"Listening to {activity.title} by {activity.artist}")
            elif isinstance(activity, discord.CustomActivity):
                activities.append(activity.name)
        
        status_text = f"{status_emojis.get(member.status, '⚫')} {str(member.status).title()}"
        if activities:
            status_text += f"\n{chr(8226)} " + f"\n{chr(8226)} ".join(activities)
        
        embed.add_field(
            name="Presence",
            value=status_text,
            inline=False
        )
        
        # Roles
        roles = [role.mention for role in reversed(member.roles) if role != ctx.guild.default_role]
        if roles:
            embed.add_field(
                name=f"Roles ({len(roles)})",
                value=" ".join(roles) if len(roles) <= 10 else " ".join(roles[:10]) + "...",
                inline=False
            )
        
        # Permissions
        key_perms = [
            "administrator", "manage_guild", "manage_roles", "manage_channels",
            "manage_messages", "manage_nicknames", "kick_members", "ban_members"
        ]
        
        perms = []
        for perm, value in member.guild_permissions:
            if value and perm in key_perms:
                perms.append(perm.replace("_", " ").title())
        
        if perms:
            embed.add_field(
                name="Key Permissions",
                value="\n".join(f"✅ {perm}" for perm in perms),
                inline=False
            )
        
        # Set footer
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))
