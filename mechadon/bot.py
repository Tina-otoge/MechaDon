import logging

import discord
from discord.ext import commands

from .db          import DBInterface
from .embed       import MechaEmbed
from .extensions  import cogs

class MechaDon(commands.Bot):

    def __init__(self, config):
        self.db_path = config.db_path

        super().__init__(command_prefix=commands.when_mentioned_or('!'))

        for cog in cogs:
            self.add_cog(cog(self))

        with open('init.sql') as f:
            with self.db() as db:
                db.execute(f.read())

        self.run(config.token)

    async def on_ready(self):
        logging.info('Bot {0.name}#{0.discriminator} ({0.id})'.format(self.user))

    def db(self):
        return DBInterface(self.db_path)

