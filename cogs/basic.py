from discord.ext import commands
import discord

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Recieve a response to test the bot to see if it's working", brief="Test the bot")
    async def ping(self, ctx):
        await ctx.send('Pong!')

def setup(bot):
    bot.add_cog(Basic(bot))
