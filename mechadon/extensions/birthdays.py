import collections
from datetime import datetime

from discord.ext import commands, tasks
from dateutil.parser import parse

from mechadon.embed import MechaEmbed
from .string import listify
from .time import DATE_BACK, DATE_FRONT

class Birthdays(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['birthday'])
    async def bday(self, context, *, date: str = None):
        if date is None:
            await self.get_bday(context)
            return
        try:
            date = parse(date)
        except ValueError:
            await context.send(
                'Sorrymasen.... I do not understand what day this is da-don....'
            )
            return
        with self.bot.db() as db:
            db.set('birthdays', context.author.id, {
                'id': context.author.id,
                'date': date.strftime(DATE_BACK)
            })
            db.commit()
        await context.send(
            'I\'ll remember your birthday as {} da-don~'.format(
                date.strftime(DATE_FRONT)
            )
        )

    @commands.command()
    @commands.guild_only()
    async def bdays(self, context, n: int = 5):
        def to_power(date):
            return int(date[5:].replace('-', ''))
        with self.bot.db() as db:
            entries = db.get('birthdays', [m.id for m in context.guild.members])
            today_power = to_power(datetime.now().strftime(DATE_BACK))
            ranking = {}
            for e in entries:
                relative_power = to_power(e['date']) - today_power
                if relative_power < 0:
                    relative_power += 1212
                ranking[relative_power] = e
            ranking = sorted(ranking.items())[:n]
            ranking = dict(ranking)
            results = [
                '{0}: {1.display_name}'.format(
                    datetime.strptime(x['date'], DATE_BACK).strftime('%B %-d'),
                    context.guild.get_member(x['id'])
                )
                for x in ranking.values()
            ]
            await context.send(embed=MechaEmbed(
                title='Upcoming birthdays',
                description=listify(results),
                context=context
            ))

    async def get_bday(self, context):
        with self.bot.db() as db:
            result = db.get('birthdays', context.author.id)
            if len(result) == 0:
                await context.send(
                    'You did not tell me your birthday yet da-don....'
                    '\nYou can do so with `!bday <date>`'
                )
                return
            date = datetime.strptime(result[0]['date'], DATE_BACK)
            await context.send(embed=MechaEmbed(
                title='{0.display_name}\'s birthday 🎂'.format(context.author),
                description=date.strftime(DATE_FRONT),
                context=context
            ))
