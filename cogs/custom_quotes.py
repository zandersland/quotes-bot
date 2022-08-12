from discord.ext import commands
import discord
import json
import os
import random
import asyncio
import time


class CustomQuotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # File operation functions

    def load_quotes(self, guild_id):
        print("Loading quotes for guild {}".format(guild_id))
        with open('data/custom_quotes.json', 'r') as f:
            quotes = json.load(f)
        if guild_id not in quotes["custom_quotes"]:
            self.add_guild_id(guild_id)
            with open('data/custom_quotes.json') as f:
                quotes = json.load(f)
        return quotes["custom_quotes"][guild_id]

    def add_guild_id(self, guild_id):
        print("Adding guild {}".format(guild_id))
        with open('data/custom_quotes.json', 'r') as f:
            quotes = json.load(f)
        quotes["custom_quotes"][guild_id] = []
        # quotes["custom_quotes"].append({f"{guild_id}": []})
        with open('data/custom_quotes.json', 'w') as f:
            json.dump(quotes, f)

    def write_quotes(self, guild_id, new_quotes):
        print("Writing quotes for guild {}".format(guild_id))
        with open('data/custom_quotes.json', 'r') as f:
            quotes = json.load(f)
        quotes["custom_quotes"][guild_id] = new_quotes
        with open('data/custom_quotes.json', 'w') as f:
            json.dump(quotes, f)

    # Command functions

    @commands.command()
    async def add_quote(self, ctx, *, quote):
        print("Adding quote for guild {}".format(ctx.guild.id))
        quotes = self.load_quotes(str(ctx.guild.id))
        quotes.append(quote)
        self.write_quotes(str(ctx.guild.id), quotes)
        await ctx.send("Quote added! :thumbsup:")


    @commands.command()
    async def remove_quote(self, ctx, *, quote):
        print("Removing quote for guild {}".format(ctx.guild.id))
        quotes = self.load_quotes(str(ctx.guild.id))
        quotes.remove(quote)
        self.write_quotes(str(ctx.guild.id), quotes)
        await ctx.send("Quote removed! :thumbsup:")

    @commands.command()
    async def list_quotes(self, ctx):
        print("Listing quotes for guild {}".format(ctx.guild.id))
        quotes = self.load_quotes(str(ctx.guild.id))
        # embed = discord.Embed(title="Custom Quotes", description="Here are the custom quotes for this server:", color=discord.Color.blurple())
        # for quote, location in zip(quotes, range(1, len(quotes) + 1)):
            # embed.add_field(name=location, value=quote, inline=False)
        # await ctx.send(embed=embed)
        
        # await ctx.send("This command is not yet implemented")
        buttons = [u"\u23EA", u"\u25C0", u"\u25B6", u"\u23E9"]
        current = 0
        msg = await ctx.send(embed=discord.Embed(title="Custom Quotes", description=f"Here are the custom quotes for this server:\n{quotes[current]}", color=discord.Color.blurple()))
        await msg.edit(embed=msg.embeds[0].set_footer(text=f"Page {current + 1}/{len(quotes)}"))

        for button in buttons:
            await msg.add_reaction(button)
            # time.sleep(0.10)

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0)
                if user != ctx.author:
                    continue
                if reaction.emoji == buttons[0]:
                    current = 0
                    await msg.edit(embed=discord.Embed(title="Custom Quotes", description=f"Here are the custom quotes for this server:\n{quotes[current]}", color=discord.Color.blurple()))
                    await msg.edit(embed=msg.embeds[0].set_footer(text=f"Page {current + 1}/{len(quotes)}"))
                    await msg.remove_reaction(reaction.emoji, user)
                elif reaction.emoji == buttons[1]:
                    current = max(0, current - 1)
                    await msg.edit(embed=discord.Embed(title="Custom Quotes", description=f"Here are the custom quotes for this server:\n{quotes[current]}", color=discord.Color.blurple()))
                    await msg.edit(embed=msg.embeds[0].set_footer(text=f"Page {current + 1}/{len(quotes)}"))
                    await msg.remove_reaction(reaction.emoji, user)
                elif reaction.emoji == buttons[2]:
                    current = min(len(quotes) - 1, current + 1)
                    await msg.edit(embed=discord.Embed(title="Custom Quotes", description=f"Here are the custom quotes for this server:\n{quotes[current]}", color=discord.Color.blurple()))
                    await msg.edit(embed=msg.embeds[0].set_footer(text=f"Page {current + 1}/{len(quotes)}"))
                    await msg.remove_reaction(reaction.emoji, user)
                elif reaction.emoji == buttons[3]:
                    current = len(quotes) - 1
                    await msg.edit(embed=discord.Embed(title="Custom Quotes", description=f"Here are the custom quotes for this server:\n{quotes[current]}", color=discord.Color.blurple()))
                    await msg.edit(embed=msg.embeds[0].set_footer(text=f"Page {current + 1}/{len(quotes)}"))
                    await msg.remove_reaction(reaction.emoji, user)
            except asyncio.TimeoutError:
                await msg.edit(embed=discord.Embed(title="Custom Quotes", description="*Timed out*", color=discord.Color.blurple()))
                await msg.clear_reactions()
                return
            # finally:
        


    @commands.command()
    async def random_quote(self, ctx):
        print("Random quote for guild {}".format(ctx.guild.id))
        quotes = self.load_quotes(str(ctx.guild.id))
        random_quote = random.choice(quotes)
        response_message = f"*\"{random_quote[0]}\"* - **{random_quote[1]}**"
        await ctx.send(response_message)



def setup(bot):
    bot.add_cog(CustomQuotes(bot))
