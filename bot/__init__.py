# -*- coding: utf-8 -*-

import asyncio

from houdini.plugins import IPlugin

from .bot import setup

TOKEN = "YOUR BOT TOKEN HERE"

class DiscordBot(IPlugin):
    author = "Connor800"
    description = "Plugin to start a bot along with Houdini"

    def __init__(self, server):
        self.loop = loop = asyncio.get_event_loop()
        self.bot = setup(server, loop)

        super().__init__(server)

    async def ready(self):
        bot = self.bot
        self.server.logger.info("Starting Discord bot: %r", bot)
        loop = self.loop

        async def runner():
            try:
                await bot.start(TOKEN)
            except KeyboardInterrupt:
                await bot.close()

        loop.create_task(runner())
