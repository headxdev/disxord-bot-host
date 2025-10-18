"""
Standard Command Template: Moderation Base
Category: Moderation
Author: headx - the psychon
Description: Basic moderation commands (kick, ban, mute, unmute, warn)
"""

import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
from typing import Optional
import json
import os

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns_file = 'data/warns.json'
        self.warns = self.load_warns()
        
    def load_warns(self):
        """Load warnings from JSON file"""
        if not os.path.exists('data'):
            os.makedirs('data')
        if os.path.exists(self.warns_file):
            with open(self.warns_file, 'r') as f:
                return json.load(f)
        return {}
        
    def save_warns(self):
        """Save warnings to JSON file"""
        with open(self.warns_file, 'w') as f:
            json.dump(self.warns, f, indent=4)

    async def log_action(self, guild, action, target, moderator, reason=None, duration=None):
        """Log moderation action to logging channel"""
        log_channel = discord.utils.get(guild.channels, name="mod-logs")
        if not log_channel:
            return
            
        embed = discord.Embed(
            title=f"Moderation Action: {action}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="Target", value=f"{target} ({target.id})", inline=True)
        embed.add_field(name="Moderator", value=f"{moderator} ({moderator.id})", inline=True)
        if duration:
            embed.add_field(name="Duration", value=str(duration), inline=True)
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
            
        embed.set_thumbnail(url=target.display_avatar.url)
        await log_channel.send(embed=embed)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """
        Kick a member from the server
        Usage: !kick @user [reason]
        """
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("You can't kick someone with a higher or equal role!")
            
        try:
            # DM user about kick
            embed = discord.Embed(
                title="You've been kicked!",
                description=f"You were kicked from {ctx.guild.name}",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason)
            embed.set_footer(text=f"Kicked by {ctx.author}")
            try:
                await member.send(embed=embed)
            except:
                pass  # Can't DM user
                
            # Kick member
            await member.kick(reason=f"{reason} - By {ctx.author}")
            
            # Send confirmation
            confirm = discord.Embed(
                title="Member Kicked",
                description=f"{member.mention} has been kicked",
                color=discord.Color.green()
            )
            confirm.add_field(name="Reason", value=reason)
            await ctx.send(embed=confirm)
            
            # Log action
            await self.log_action(ctx.guild, "Kick", member, ctx.author, reason)
            
        except Exception as e:
            await ctx.send(f"Error kicking member: {e}")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, delete_days: Optional[int] = 0, *, reason: Optional[str] = "No reason provided"):
        """
        Ban a member from the server
        Usage: !ban @user [delete_messages_days] [reason]
        """
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("You can't ban someone with a higher or equal role!")
            
        delete_days = min(7, max(0, delete_days))  # Clamp between 0 and 7
            
        try:
            # DM user about ban
            embed = discord.Embed(
                title="You've been banned!",
                description=f"You were banned from {ctx.guild.name}",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason)
            embed.set_footer(text=f"Banned by {ctx.author}")
            try:
                await member.send(embed=embed)
            except:
                pass  # Can't DM user
                
            # Ban member
            await member.ban(reason=f"{reason} - By {ctx.author}", delete_message_days=delete_days)
            
            # Send confirmation
            confirm = discord.Embed(
                title="Member Banned",
                description=f"{member.mention} has been banned",
                color=discord.Color.green()
            )
            confirm.add_field(name="Reason", value=reason)
            confirm.add_field(name="Deleted Messages", value=f"{delete_days} days")
            await ctx.send(embed=confirm)
            
            # Log action
            await self.log_action(ctx.guild, "Ban", member, ctx.author, reason)
            
        except Exception as e:
            await ctx.send(f"Error banning member: {e}")

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """
        Mute a member (prevent them from sending messages)
        Usage: !mute @user [reason]
        """
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("You can't mute someone with a higher or equal role!")
            
        # Get or create muted role
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            try:
                muted_role = await ctx.guild.create_role(
                    name="Muted",
                    reason="Mute command setup"
                )
                
                # Set permissions for all channels
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, speak=False, send_messages=False, add_reactions=False)
            except Exception as e:
                return await ctx.send(f"Error creating muted role: {e}")
                
        try:
            if muted_role in member.roles:
                return await ctx.send(f"{member.mention} is already muted!")
                
            # Mute member
            await member.add_roles(muted_role, reason=f"{reason} - By {ctx.author}")
            
            # Send confirmation
            embed = discord.Embed(
                title="Member Muted",
                description=f"{member.mention} has been muted",
                color=discord.Color.orange()
            )
            embed.add_field(name="Reason", value=reason)
            await ctx.send(embed=embed)
            
            # Log action
            await self.log_action(ctx.guild, "Mute", member, ctx.author, reason)
            
        except Exception as e:
            await ctx.send(f"Error muting member: {e}")

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """
        Unmute a member
        Usage: !unmute @user [reason]
        """
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            return await ctx.send("No muted role found!")
            
        if muted_role not in member.roles:
            return await ctx.send(f"{member.mention} is not muted!")
            
        try:
            # Unmute member
            await member.remove_roles(muted_role, reason=f"{reason} - By {ctx.author}")
            
            # Send confirmation
            embed = discord.Embed(
                title="Member Unmuted",
                description=f"{member.mention} has been unmuted",
                color=discord.Color.green()
            )
            embed.add_field(name="Reason", value=reason)
            await ctx.send(embed=embed)
            
            # Log action
            await self.log_action(ctx.guild, "Unmute", member, ctx.author, reason)
            
        except Exception as e:
            await ctx.send(f"Error unmuting member: {e}")

    @commands.command(name="warn")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        """
        Warn a member
        Usage: !warn @user <reason>
        """
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("You can't warn someone with a higher or equal role!")
            
        # Initialize warns for guild if not exists
        guild_id = str(ctx.guild.id)
        if guild_id not in self.warns:
            self.warns[guild_id] = {}
            
        # Initialize warns for user if not exists
        user_id = str(member.id)
        if user_id not in self.warns[guild_id]:
            self.warns[guild_id][user_id] = []
            
        # Add warning
        warning = {
            "reason": reason,
            "moderator": ctx.author.id,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.warns[guild_id][user_id].append(warning)
        self.save_warns()
        
        # Send confirmation
        embed = discord.Embed(
            title="Member Warned",
            description=f"{member.mention} has been warned",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Reason", value=reason)
        embed.add_field(
            name="Total Warnings",
            value=len(self.warns[guild_id][user_id]),
            inline=False
        )
        await ctx.send(embed=embed)
        
        # DM user
        try:
            warn_dm = discord.Embed(
                title="You've been warned!",
                description=f"You received a warning in {ctx.guild.name}",
                color=discord.Color.yellow()
            )
            warn_dm.add_field(name="Reason", value=reason)
            warn_dm.set_footer(text=f"Warned by {ctx.author}")
            await member.send(embed=warn_dm)
        except:
            pass
            
        # Log action
        await self.log_action(ctx.guild, "Warn", member, ctx.author, reason)

    @commands.command(name="warnings", aliases=["warns"])
    @commands.has_permissions(kick_members=True)
    async def warnings(self, ctx, member: discord.Member):
        """
        Show warnings for a member
        Usage: !warnings @user
        """
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        
        if guild_id not in self.warns or user_id not in self.warns[guild_id]:
            return await ctx.send(f"{member.mention} has no warnings!")
            
        warnings = self.warns[guild_id][user_id]
        
        embed = discord.Embed(
            title=f"Warnings for {member}",
            color=discord.Color.yellow()
        )
        
        for i, warning in enumerate(warnings, 1):
            moderator = ctx.guild.get_member(warning["moderator"])
            mod_name = moderator.name if moderator else "Unknown Moderator"
            timestamp = datetime.fromisoformat(warning["timestamp"])
            
            embed.add_field(
                name=f"Warning #{i}",
                value=f"**Reason:** {warning['reason']}\n"
                      f"**By:** {mod_name}\n"
                      f"**When:** {discord.utils.format_dt(timestamp, 'R')}",
                inline=False
            )
            
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
