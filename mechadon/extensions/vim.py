import discord
from discord.ext import commands

from mechadon.embed import MechaEmbed
from mechadon.errors import ThinkingError

class Vim(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vim(self, context, *, tag):
        with self.bot.db(self.bot.config.vim_db_path) as db:
            results = db.get('tags', {'name': tag})
            if len(results) is 0:
                raise ThinkingError
            tag = results[0]
            results = db.get('help', tag['help_id'])
            if len(results) is 0:
                await context.send(embed=MechaEmbed(
                    description=
                        'An entry for this tag exists but it\'s empty\n'
                        'Maybe it has subtags, try a more precise one!',
                    context=context
                ))
                return
            await context.send('```\n{}\n```'.format(results[0]['content']))


