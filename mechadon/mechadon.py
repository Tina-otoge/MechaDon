from discord.ext import commands
from . import cogs
from .dbinterface import DBInterface

class MechaDon(commands.Bot):

    def __init__(self, config):
        super().__init__(command_prefix=commands.when_mentioned_or('!'))

        self.add_cog(cogs.SelfRoles(self))

        DBInterface.db_path = config.db_path
        with open('init.sql') as f:
            with DBInterface() as db:
                db.execute(f.read())

        self.run(config.token)

    async def on_ready(self):
        print('Bot ready')
        print('{0.name}#{0.discriminator} ({0.id})'.format(self.user))
