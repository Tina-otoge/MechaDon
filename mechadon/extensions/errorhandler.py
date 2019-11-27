import logging
import traceback

import discord
from discord.ext import commands

from mechadon.embed import MechaEmbed
from mechadon.errors import ThinkingError

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.errors.CommandInvokeError):
            exception = exception.original
        if isinstance(exception, (
            commands.errors.CommandNotFound,
            ThinkingError
        )):
            logging.info('Ignoring exception: ' + str(exception))
            await context.message.add_reaction('🤔')
            return
        logging.info('Reporting {0.__class__.__name__}: {0}'.format(
            exception,
        ))
        embed = {
            'title': '*Dongyaa--!! An error occured da-don!*',
            'colour': discord.Colour.orange(),
            'description' : str(exception),
            'context': context
        }
        await context.send(embed=MechaEmbed(**embed))
