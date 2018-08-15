from discord.ext import commands

from .ext         import cogs
from .dbinterface import DBInterface
from .mechaembed  import MechaEmbed

class MechaDon(commands.Bot):

    def __init__(self, config):
        self.db_path = config.db_path

        super().__init__(command_prefix=commands.when_mentioned_or('!'))

        for cog in cogs:
            self.add_cog(cog(self))

        with open('init.sql') as f:
            with self.db_interface() as db:
                db.execute(f.read())

        self.run(config.token)

    async def on_ready(self):
        print('Bot ready')
        print('{0.name}#{0.discriminator} ({0.id})'.format(self.user))

    def create_embed(self, **kwargs):
        return MechaEmbed(**kwargs)

    def db_interface(self):
        return DBInterface(self.db_path)
