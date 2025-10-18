from discord.ext import commands
import discord
from datetime import datetime

class ExampleCog(commands.Cog):
    """Example cog with useful basic commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="ping", description="Check bot latency")
    async def ping(self, ctx):
        """Check the bot's latency"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: {latency}ms",
            color=discord.Color.green() if latency < 100 else discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @commands.command(name="info", description="Show bot information")
    async def info(self, ctx):
        """Display information about the bot"""
        embed = discord.Embed(
            title="Bot Information",
            description="Discord Bot Manager by headx - the psychon",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Python Version", value=discord.version_info)
        embed.add_field(name="Discord.py Version", value=discord.__version__)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        await ctx.send(embed=embed)

    @commands.command(name="help", description="Show help for commands")
    async def custom_help(self, ctx, command_name: str = None):
        """Show help information for commands"""
        if command_name:
            cmd = self.bot.get_command(command_name)
            if not cmd:
                return await ctx.send(f"Command `{command_name}` not found!")
            
            embed = discord.Embed(
                title=f"Help: {cmd.name}",
                description=cmd.help or "No description available",
                color=discord.Color.blue()
            )
            if cmd.aliases:
                embed.add_field(name="Aliases", value=", ".join(cmd.aliases))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Available Commands",
                description="Use `!help <command>` for detailed information",
                color=discord.Color.blue()
            )
            for cog_name, cog in self.bot.cogs.items():
                cmd_list = [f"`{c.name}`" for c in cog.get_commands()]
                if cmd_list:
                    embed.add_field(name=cog_name, value=" ".join(cmd_list), inline=False)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Welcome new members"""
        channel = member.guild.system_channel
        if channel:
            embed = discord.Embed(
                title="Welcome!",
                description=f"Welcome {member.mention} to {member.guild.name}!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            await channel.send(embed=embed)

    @commands.command(name="serverinfo", description="Show server information")
    async def serverinfo(self, ctx):
        """Display information about the current server"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"{guild.name} Server Information",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Owner", value=guild.owner.mention)
        embed.add_field(name="Created", value=guild.created_at.strftime("%d.%m.%Y"))
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Channels", value=len(guild.channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.set_footer(text=f"ID: {guild.id}")
        await ctx.send(embed=embed)

def setup(bot):
    """Add this cog to the bot"""
    bot.add_cog(ExampleCog(bot))