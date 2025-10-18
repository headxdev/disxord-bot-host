"""
Command Template: Music
Category: Entertainment
Author: headx - the psychon
Description: Basic music commands for playing audio in voice channels
"""

import discord
from discord.ext import commands
import asyncio
from collections import deque

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}  # Guild ID -> Queue
        self.now_playing = {}  # Guild ID -> Current Song

    def get_queue(self, guild_id):
        """Get or create queue for guild"""
        if guild_id not in self.queues:
            self.queues[guild_id] = deque()
        return self.queues[guild_id]

    @commands.command(name="join")
    async def join(self, ctx):
        """Join your voice channel"""
        if not ctx.author.voice:
            return await ctx.send("You need to be in a voice channel!")
        
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        
        await ctx.send(embed=discord.Embed(
            title="🎵 Joined Voice Channel",
            description=f"Connected to {channel.name}",
            color=discord.Color.green()
        ))

    @commands.command(name="play")
    async def play(self, ctx, *, query):
        """
        Add a song to the queue
        Usage: !play <song name or URL>
        """
        if not ctx.voice_client:
            await ctx.invoke(self.join)
        
        # For this template, we'll just simulate adding to queue
        queue = self.get_queue(ctx.guild.id)
        queue.append(query)
        
        embed = discord.Embed(
            title="🎵 Added to Queue",
            description=f"Added: {query}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Position", value=len(queue))
        await ctx.send(embed=embed)

    @commands.command(name="queue")
    async def queue(self, ctx):
        """Show the current queue"""
        queue = self.get_queue(ctx.guild.id)
        if not queue:
            return await ctx.send("Queue is empty!")
        
        embed = discord.Embed(
            title="🎵 Current Queue",
            color=discord.Color.blue()
        )
        
        for i, song in enumerate(queue, 1):
            embed.add_field(
                name=f"{i}. {song}",
                value="Queued",
                inline=False
            )
        
        await ctx.send(embed=embed)

    @commands.command(name="skip")
    async def skip(self, ctx):
        """Skip the current song"""
        queue = self.get_queue(ctx.guild.id)
        if not queue:
            return await ctx.send("Nothing to skip!")
        
        if queue:
            skipped = queue.popleft()
            await ctx.send(embed=discord.Embed(
                title="⏭️ Skipped",
                description=f"Skipped: {skipped}",
                color=discord.Color.blue()
            ))

    @commands.command(name="stop")
    async def stop(self, ctx):
        """Stop playing and clear the queue"""
        queue = self.get_queue(ctx.guild.id)
        queue.clear()
        
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        
        await ctx.send(embed=discord.Embed(
            title="⏹️ Stopped",
            description="Music playback stopped and queue cleared",
            color=discord.Color.red()
        ))

def setup(bot):
    bot.add_cog(Music(bot))
