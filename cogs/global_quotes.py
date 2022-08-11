from discord.ext import commands
import random
import json

class GlobalQuotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random_global_quote(self, ctx):
        with open('default_quotes.json') as f:
            quotes = json.load(f)
        random_quote = random.choice(quotes["default_quotes"])
        response_message = f"*\"{random_quote[0]}\"* - **{random_quote[1]}**"
        await ctx.send(response_message)


def setup(bot):
    bot.add_cog(GlobalQuotes(bot))
