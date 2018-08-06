import discord
from discord.ext import commands

import cogs
import config

bot = commands.Bot(command_prefix=commands.when_mentioned)

bot.add_cog(cogs.SelfRoles(bot))
print('Initiating bot')
bot.run(config.token)
