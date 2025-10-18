"""
Standard Command Template: Avatar
Category: Basic
Author: headx - the psychon
"""

import discord
from discord.ext import commands
from typing import Optional

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar", aliases=["av", "pfp"])
    async def avatar(self, ctx, member: Optional[discord.Member] = None):
        """
        Show user's avatar in different formats
        Usage: !avatar [@user]
        """
        member = member or ctx.author
        
        # Create embed
        embed = discord.Embed(
            title=f"Avatar for {member.display_name}",
            color=member.color if member.color != discord.Color.default() else discord.Color.blue()
        )
        
        # Add server-specific avatar if different from global
        if member.guild_avatar:
            embed.add_field(
                name="Server Avatar",
                value=f"[PNG]({member.guild_avatar.replace(format='png', size=1024)}) | "
                      f"[JPG]({member.guild_avatar.replace(format='jpg', size=1024)}) | "
                      f"[WEBP]({member.guild_avatar.replace(format='webp', size=1024)})",
                inline=False
            )
            embed.set_thumbnail(url=member.guild_avatar.url)
        
        # Add global avatar
        embed.add_field(
            name="Global Avatar",
            value=f"[PNG]({member.display_avatar.replace(format='png', size=1024)}) | "
                  f"[JPG]({member.display_avatar.replace(format='jpg', size=1024)}) | "
                  f"[WEBP]({member.display_avatar.replace(format='webp', size=1024)})",
            inline=False
        )
        
        # If no server avatar, use global avatar as thumbnail
        if not member.guild_avatar:
            embed.set_thumbnail(url=member.display_avatar.url)
        
        # Set large image preview
        embed.set_image(url=member.display_avatar.replace(size=1024).url)
        
        # Add footer
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )
        
        # Add buttons for easy format switching
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="PNG",
                url=member.display_avatar.replace(format='png', size=1024).url
            )
        )
        view.add_item(
            discord.ui.Button(
                label="JPG",
                url=member.display_avatar.replace(format='jpg', size=1024).url
            )
        )
        view.add_item(
            discord.ui.Button(
                label="WEBP",
                url=member.display_avatar.replace(format='webp', size=1024).url
            )
        )
        
        await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Avatar(bot))
