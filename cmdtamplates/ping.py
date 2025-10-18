#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord Bot Manager - Ping Command Template
Enhanced ping command with latency information and status.

@author headx & the psychon
@version 2.0
"""

import discord
from discord.ext import commands
import time
import platform
import psutil
from datetime import datetime, timedelta


class PingCommand(commands.Cog):
    """Advanced ping command with system information."""
    
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()
    
    @commands.command(name='ping', aliases=['pong', 'latency'])
    async def ping(self, ctx):
        """
        Shows bot latency and system information.
        
        Usage: !ping
        """
        # Measure message round-trip time
        start_time = time.perf_counter()
        message = await ctx.send("🏓 Pinging...")
        end_time = time.perf_counter()
        
        # Calculate latencies
        websocket_latency = round(self.bot.latency * 1000, 2)
        message_latency = round((end_time - start_time) * 1000, 2)
        
        # Get system info
        uptime = datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0]  # Remove microseconds
        
        # Create embed
        embed = discord.Embed(
            title="🏓 Pong!",
            description="Bot status and latency information",
            color=discord.Color.green() if websocket_latency < 100 else 
                  discord.Color.yellow() if websocket_latency < 250 else 
                  discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        # Add latency fields
        embed.add_field(
            name="🌐 WebSocket Latency",
            value=f"`{websocket_latency}ms`",
            inline=True
        )
        
        embed.add_field(
            name="📨 Message Latency",
            value=f"`{message_latency}ms`",
            inline=True
        )
        
        embed.add_field(
            name="⏰ Uptime",
            value=f"`{uptime_str}`",
            inline=True
        )
        
        # Add system info
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            embed.add_field(
                name="💻 System Info",
                value=f"**CPU:** `{cpu_percent}%`\n"
                      f"**RAM:** `{memory.percent}%`\n"
                      f"**OS:** `{platform.system()}`",
                inline=True
            )
        except ImportError:
            # psutil not available
            embed.add_field(
                name="💻 System Info",
                value="System info not available\n*(Install psutil for details)*",
                inline=True
            )
        
        # Add bot info
        embed.add_field(
            name="📊 Bot Stats",
            value=f"**Servers:** `{len(self.bot.guilds)}`\n"
                  f"**Users:** `{len(self.bot.users)}`\n"
                  f"**Commands:** `{len(self.bot.commands)}`",
            inline=True
        )
        
        # Add status indicators
        status_emoji = {
            'online': '🟢',
            'idle': '🟡',
            'dnd': '🔴',
            'invisible': '⚫'
        }
        
        embed.set_footer(
            text=f"Status: {status_emoji.get(str(self.bot.status), '⚪')} {self.bot.status.name.title()}"
        )
        
        # Edit the original message
        await message.edit(content=None, embed=embed)
    
    @commands.command(name='status', aliases=['info', 'stats'])
    async def status(self, ctx):
        """
        Shows detailed bot status information.
        
        Usage: !status
        """
        uptime = datetime.now() - self.start_time
        
        embed = discord.Embed(
            title="🤖 Bot Status",
            description=f"**{self.bot.user.name}** is online and running",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        # Bot information
        embed.add_field(
            name="🏷️ Bot Info",
            value=f"**Name:** {self.bot.user.name}\n"
                  f"**ID:** {self.bot.user.id}\n"
                  f"**Created:** <t:{int(self.bot.user.created_at.timestamp())}:R>",
            inline=False
        )
        
        # Statistics
        embed.add_field(
            name="📊 Statistics",
            value=f"**Servers:** {len(self.bot.guilds)}\n"
                  f"**Users:** {len(self.bot.users)}\n"
                  f"**Text Channels:** {sum(len(guild.text_channels) for guild in self.bot.guilds)}\n"
                  f"**Voice Channels:** {sum(len(guild.voice_channels) for guild in self.bot.guilds)}",
            inline=True
        )
        
        # Performance
        embed.add_field(
            name="⚡ Performance",
            value=f"**Latency:** {round(self.bot.latency * 1000, 2)}ms\n"
                  f"**Uptime:** {str(uptime).split('.')[0]}\n"
                  f"**Commands:** {len(self.bot.commands)}",
            inline=True
        )
        
        # Add thumbnail
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        
        embed.set_footer(
            text=f"Discord Bot Manager v2.0 • Python {platform.python_version()}"
        )
        
        await ctx.send(embed=embed)


def setup(bot):
    """Load the PingCommand cog."""
    bot.add_cog(PingCommand(bot))


# Standalone command function (for non-cog usage)
async def ping_command(bot, ctx):
    """
    Simple ping command without cog structure.
    
    Args:
        bot: Discord bot instance
        ctx: Command context
    """
    start_time = time.perf_counter()
    message = await ctx.send("🏓 Pinging...")
    end_time = time.perf_counter()
    
    websocket_latency = round(bot.latency * 1000, 2)
    message_latency = round((end_time - start_time) * 1000, 2)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        color=discord.Color.green() if websocket_latency < 100 else 
              discord.Color.yellow() if websocket_latency < 250 else 
              discord.Color.red()
    )
    
    embed.add_field(
        name="Latency",
        value=f"WebSocket: `{websocket_latency}ms`\nMessage: `{message_latency}ms`",
        inline=False
    )
    
    await message.edit(content=None, embed=embed)


# Command template metadata for the Bot Manager
TEMPLATE_INFO = {
    "name": "ping",
    "description": "Enhanced ping command with latency and system information",
    "category": "Utility",
    "usage": "!ping, !status",
    "aliases": ["pong", "latency", "status", "info", "stats"],
    "permissions": [],
    "cooldown": 5,
    "version": "2.0",
    "author": "headx & the psychon",
    "dependencies": ["psutil (optional)"],
    "features": [
        "WebSocket latency measurement",
        "Message round-trip time",
        "Bot uptime tracking",
        "System resource monitoring",
        "Detailed bot statistics",
        "Colorized latency indicators",
        "Multiple command aliases"
    ]
}