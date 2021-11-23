import discord
from discord.ext import commands


def caps_pls(text):
    return text.upper()


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def say(self, ctx, *, arg):
        await ctx.send(arg)

    """@say.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Bitte gebe an, was ich sagen soll.')"""

    @commands.command()
    async def caps(self, ctx, *, arg: caps_pls):
        await ctx.send(arg)

    @caps.error
    async def caps_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Bitte gebe an, was ich schreien soll.')

    @commands.command()
    async def kill(self, ctx, member: discord.Member):
        await ctx.send(f'{member.display_name} wurde gekillt.')

    @kill.error
    async def kill_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Ich kann ihn nicht finden sry.')


def setup(client):
    client.add_cog(Commands(client))