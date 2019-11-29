import logging

import discord
from discord.ext import commands

from .db          import DBInterface
from .embed       import MechaEmbed
from .extensions  import cogs

class MechaDon(commands.Bot):

    def __init__(self, config):
        self.config = config
        self.db_path = self.config.get('db_path', 'MechaDon.db')

        super().__init__(command_prefix=commands.when_mentioned_or('!'))

        for cog in cogs:
            self.add_cog(cog(self))

        with open('init.sql') as f:
            with self.db() as db:
                db.execute(f.read())

        self.run(config.get('token'))

    def config_loads(self, defaults={}, as_schema=False):
        if as_schema:
            return {k:self.config.get(k, defaults[k]) for k in defaults}
        return defaults.update(self.config)

    async def on_ready(self):
        logging.info('Bot {0.name}#{0.discriminator} ({0.id})'.format(self.user))

    def db(self, path=None):
        path = path or self.db_path
        return DBInterface(path)

