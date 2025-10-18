#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord Bot Manager - Enhanced Bot Template
Professional Discord bot template with comprehensive features.

@author headx & the psychon
@version 2.0
"""

import discord
from discord.ext import commands, tasks
import asyncio
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
import os
from typing import Optional, Union

# Enhanced logging configuration
def setup_logging(bot_name: str) -> logging.Logger:
    """Set up enhanced logging for the bot."""
    log_dir = Path(__file__).parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create logger
    logger = logging.getLogger(bot_name)
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # File handler
    file_handler = logging.FileHandler(
        log_dir / f'{bot_name}.log',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


class EnhancedBot(commands.Bot):
    """Enhanced Discord bot with additional features."""
    
    def __init__(self, config: dict, *args, **kwargs):
        self.config = config
        self.start_time = datetime.now()
        
        # Setup intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True  # Enable if needed
        intents.presences = True  # Enable if needed
        
        # Initialize bot
        super().__init__(
            command_prefix=config.get('prefix', '!'),
            intents=intents,
            help_command=commands.DefaultHelpCommand(no_category='Commands'),
            case_insensitive=True,
            strip_after_prefix=True,
            *args,
            **kwargs
        )
        
        # Setup logging
        self.logger = setup_logging(config.get('name', 'DiscordBot'))
        
        # Statistics
        self.commands_used = {}
        self.uptime = datetime.now()
    
    async def setup_hook(self):
        """Setup hook called when the bot is starting."""
        self.logger.info(f"Setting up {self.user} (ID: {self.user.id})")
        
        # Load extensions/cogs here
        # await self.load_extension('cogs.admin')
        # await self.load_extension('cogs.moderation')
        
        # Start background tasks
        self.status_task.start()
        
        # Sync slash commands if using them
        # await self.tree.sync()
        # self.logger.info("Slash commands synced")
    
    async def on_ready(self):
        """Called when the bot is ready."""
        self.logger.info(f"Bot is ready! Logged in as {self.user}")
        self.logger.info(f"Bot ID: {self.user.id}")
        self.logger.info(f"Discord.py version: {discord.__version__}")
        self.logger.info(f"Connected to {len(self.guilds)} guilds")
        self.logger.info(f"Serving {len(self.users)} users")
        
        # Set initial status
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=f"{self.command_prefix}help | v2.0")
        )
    
    async def on_command(self, ctx):
        """Called when a command is invoked."""
        command_name = ctx.command.name if ctx.command else 'unknown'
        
        # Update statistics
        if command_name not in self.commands_used:
            self.commands_used[command_name] = 0
        self.commands_used[command_name] += 1
        
        # Log command usage
        self.logger.info(
            f"Command '{command_name}' used by {ctx.author} "
            f"in {ctx.guild.name if ctx.guild else 'DM'}"
        )
    
    async def on_command_error(self, ctx, error):
        """Global error handler for commands."""
        # Ignore command not found errors
        if isinstance(error, commands.CommandNotFound):
            return
        
        # Handle specific errors
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"❌ Missing required argument: `{error.param.name}`\n"
                f"Usage: `{ctx.command.signature}`"
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"❌ You don't have permission to use this command.\n"
                f"Required permissions: {', '.join(error.missing_permissions)}"
            )
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                f"❌ I don't have permission to do that.\n"
                f"Required permissions: {', '.join(error.missing_permissions)}"
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"⏰ This command is on cooldown. "
                f"Try again in {error.retry_after:.2f} seconds."
            )
        else:
            # Log unexpected errors
            self.logger.error(
                f"Unexpected error in command '{ctx.command}': {error}\n"
                f"{''.join(traceback.format_exception(type(error), error, error.__traceback__))}"
            )
            await ctx.send(
                "❌ An unexpected error occurred. Please try again later."
            )
    
    async def on_error(self, event, *args, **kwargs):
        """Global error handler for events."""
        self.logger.error(f"Error in event '{event}': {traceback.format_exc()}")
    
    @tasks.loop(minutes=30)
    async def status_task(self):
        """Background task to update bot status."""
        statuses = [
            f"{self.command_prefix}help | v2.0",
            f"Serving {len(self.guilds)} servers",
            f"Watching {len(self.users)} users",
            "Discord Bot Manager"
        ]
        
        for status in statuses:
            await self.change_presence(
                activity=discord.Game(name=status)
            )
            await asyncio.sleep(300)  # 5 minutes
    
    @status_task.before_loop
    async def before_status_task(self):
        """Wait until bot is ready before starting status task."""
        await self.wait_until_ready()


# Basic Commands
@commands.command(name='info', aliases=['about', 'botinfo'])
async def bot_info(ctx):
    """Display bot information."""
    bot = ctx.bot
    uptime = datetime.now() - bot.start_time
    
    embed = discord.Embed(
        title="🤖 Bot Information",
        description=bot.config.get('description', 'A Discord bot created with Discord Bot Manager'),
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="📊 Statistics",
        value=f"**Servers:** {len(bot.guilds)}\n"
              f"**Users:** {len(bot.users)}\n"
              f"**Commands:** {len(bot.commands)}\n"
              f"**Uptime:** {str(uptime).split('.')[0]}",
        inline=True
    )
    
    embed.add_field(
        name="⚡ Performance",
        value=f"**Latency:** {round(bot.latency * 1000, 2)}ms\n"
              f"**Python:** {discord.version_info}\n"
              f"**Discord.py:** {discord.__version__}",
        inline=True
    )
    
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
    embed.set_footer(text="Discord Bot Manager v2.0")
    
    await ctx.send(embed=embed)


@commands.command(name='ping')
async def ping(ctx):
    """Check bot latency."""
    import time
    
    start = time.perf_counter()
    message = await ctx.send("🏓 Pinging...")
    end = time.perf_counter()
    
    latency = round(ctx.bot.latency * 1000, 2)
    msg_latency = round((end - start) * 1000, 2)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        color=discord.Color.green() if latency < 100 else 
              discord.Color.yellow() if latency < 250 else 
              discord.Color.red()
    )
    
    embed.add_field(
        name="Latency",
        value=f"WebSocket: `{latency}ms`\nMessage: `{msg_latency}ms`",
        inline=False
    )
    
    await message.edit(content=None, embed=embed)


async def main():
    """Main function to run the bot."""
    # Load configuration
    config_path = Path(__file__).parent / 'config.json'
    if not config_path.exists():
        print("❌ config.json not found!")
        print("Please create a config.json file with your bot settings.")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Validate required config
    if not config.get('token'):
        print("❌ Bot token not found in config.json!")
        return
    
    # Create and run bot
    bot = EnhancedBot(config)
    
    # Add commands to bot
    bot.add_command(bot_info)
    bot.add_command(ping)
    
    try:
        await bot.start(config['token'])
    except discord.LoginFailure:
        print("❌ Invalid bot token!")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
    finally:
        if not bot.is_closed():
            await bot.close()


if __name__ == "__main__":
    # Example config.json structure
    example_config = {
        "name": "My Discord Bot",
        "description": "A professional Discord bot",
        "token": "YOUR_BOT_TOKEN_HERE",
        "prefix": "!",
        "owner_id": 123456789012345678,
        "features": {
            "auto_status": True,
            "command_logging": True,
            "error_handling": True
        }
    }
    
    print("Discord Bot Manager v2.0 - Enhanced Bot Template")
    print("=" * 50)
    
    # Check if config exists
    config_path = Path(__file__).parent / 'config.json'
    if not config_path.exists():
        print("Creating example config.json...")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(example_config, f, indent=2)
        print("Please edit config.json with your bot settings and run again.")
    else:
        # Run the bot
        asyncio.run(main())