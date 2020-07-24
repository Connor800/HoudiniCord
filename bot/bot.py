# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

class Penguin(commands.Converter):
    """Converter that searches for a Spheniscidae instance.
    
    The lookup strategy is as follows (in order):

    1. Lookup by ID.
    2. Lookup by username.
    """
    @staticmethod
    async def convert(ctx, arg):
        houdini = ctx.bot.houdini
        try:
            p = houdini.penguins_by_id[int(arg)]
        except (KeyError, ValueError):
            try:
                p = houdini.penguins_by_username[arg]
            except KeyError:
                raise commands.BadArgument("No penguin found!") from None

        return p

class MyCog(commands.Cog, name="My Cog"):
    """Useful commands."""
    def __init__(self, bot, houdini):
        self.bot = bot
        self.houdini = bot.houdini = houdini # make houdini accesible when this cog isn't

    @commands.command()
    async def ping(self, ctx):
        """Measure the ping between your bot and Discord."""
        await ctx.send(f"Ping: {round(ctx.bot.latency*1000)} ms.")

    @commands.command()
    async def users(self, ctx):
        """Returns the amount of users connected to your CPPS."""
        houdini = self.houdini
        await ctx.send(f"{len(houdini.penguins_by_id)} user(s) are currently online on {houdini.config.name}!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, *, penguin: Penguin):
        """Kicks a penguin by its ID or username."""
        from houdini.handlers.play.moderation import moderator_kick
        await moderator_kick(penguin, penguin.id)
        await ctx.message.add_reaction("\N{OK HAND SIGN}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, penguin: Penguin, hours: int, *, comment=None):
        """Bans a penguin by its ID or username for a period of time and an optional reason."""
        from houdini.handlers.play.moderation import moderator_ban
        await moderator_ban(penguin, penguin.id, hours, comment or '')
        await ctx.message.add_reaction("\N{OK HAND SIGN}")

    @kick.error
    @ban.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(str(error))

def setup(server, loop):
    """Function called by the plugin to get a bot instance."""
    bot = commands.Bot("!",
        description="I'm a bot that works with Houdini Asyncio!",
        loop=loop)
    bot.add_cog(MyCog(bot, server))

    # IMPORTANT: Do NOT run the bot. The plugin will do so
    # so your CPPS can still serve your players.
    return bot
