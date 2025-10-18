"""
Command Template: Fun
Category: Entertainment
Author: headx - the psychon
Description: Collection of fun commands (8ball, dice, coin, etc.)
"""

import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._8ball_responses = [
            "It is certain", "Without a doubt", "You may rely on it",
            "Yes definitely", "It is decidedly so", "As I see it, yes",
            "Most likely", "Yes", "Outlook good", "Signs point to yes",
            "Reply hazy try again", "Better not tell you now",
            "Ask again later", "Cannot predict now",
            "Don't count on it", "My reply is no", "My sources say no",
            "Very doubtful", "Outlook not so good"
        ]

    @commands.command(name="8ball")
    async def _8ball(self, ctx, *, question):
        """
        Ask the magic 8ball a question
        Usage: !8ball <your question>
        """
        response = random.choice(self._8ball_responses)
        
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            color=discord.Color.blue()
        )
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=response, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name="roll", aliases=["dice"])
    async def roll(self, ctx, dice: str = "1d6"):
        """
        Roll dice in NdN format
        Usage: !roll [NdN] - e.g., !roll 2d20
        """
        try:
            number, sides = map(int, dice.split('d'))
            if number > 100 or sides > 100:
                return await ctx.send("Too many dice or sides! Maximum is 100.")
            
            rolls = [random.randint(1, sides) for _ in range(number)]
            
            embed = discord.Embed(
                title="🎲 Dice Roll",
                description=f"Rolling {dice}...",
                color=discord.Color.green()
            )
            embed.add_field(name="Results", value=", ".join(map(str, rolls)))
            embed.add_field(name="Total", value=sum(rolls))
            
            await ctx.send(embed=embed)
            
        except ValueError:
            await ctx.send("Format must be NdN (e.g., 2d6)")

    @commands.command(name="coin", aliases=["flip"])
    async def coin(self, ctx):
        """Flip a coin"""
        result = random.choice(["Heads", "Tails"])
        emoji = "🌝" if result == "Heads" else "🌚"
        
        embed = discord.Embed(
            title=f"{emoji} Coin Flip",
            description=f"The coin landed on: **{result}**",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @commands.command(name="choose")
    async def choose(self, ctx, *choices):
        """
        Choose between multiple options
        Usage: !choose option1 option2 [option3 ...]
        """
        if len(choices) < 2:
            return await ctx.send("Please provide at least 2 choices!")
        
        chosen = random.choice(choices)
        
        embed = discord.Embed(
            title="🤔 Choice Made",
            description=f"I choose: **{chosen}**",
            color=discord.Color.blue()
        )
        embed.add_field(name="Options were", value=", ".join(choices))
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
