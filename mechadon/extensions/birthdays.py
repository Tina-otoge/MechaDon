import collections
from datetime import datetime
import logging

import discord
from discord.ext import commands, tasks
from dateutil.parser import parse

from mechadon.embed import MechaEmbed
import mechadon.db as MDB
from .admin import is_admin
from .string import listify
from .time import DATE_BACK, DATE_FRONT

class Birthdays(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.wishes_time = self.bot.config.get('wishes_time', 0)
        self.wishes.start()

    def cog_unload(self):
        self.wishes.cancel()

    @tasks.loop(seconds=10.0)
    async def wishes(self):
        today = datetime.now()
        if self.to_power(today.strftime('%H-%M')) == self.wishes_time:
            self.wishes.change_interval(hours=24)
        else:
            return
        with self.bot.db() as db:
            today_bdays = db.get('birthdays', {
                'date': today.strftime(DATE_BACK)
            })
            bday_servers = db.get('servers', {
                'birthday_channel': MDB.NotEmpty
            }, ['id', 'birthday_channel'])
            for server in bday_servers:
                channel_id = server['birthday_channel']
                server_id = server['id']
                server = discord.utils.get(self.bot.guilds, id=server_id)
                if server is None:
                    logging.warn(
                        'Server id {} exists in DB but can not be found in the'
                        ' bot\'s servers'.format(server_id)
                    )
                    continue
                channel = discord.utils.get(server.channels, id=channel_id)
                if channel is None:
                    logging.warn(
                        'Channel id {} exists in the bot DB but can not be'
                        ' found on the server {}'.format(channel_id, server)
                    )
                    continue
                server_bdays = [
                    discord.utils.get(server.members, id=e['id'])
                    for e in today_bdays
                ]
                if len(server_bdays) is 0:
                    continue
                await channel.send(embed=MechaEmbed(
                    title='Today\'s birthdays! 🎉',
                    description=listify(server_bdays),
                    footer=self.qualified_name
                ))



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

    def to_power(self, date):
        return int(date[-5:].replace('-', ''))

    def to_bdays_list(self, bdays, id_resolver=None):
        return [
            '{0}: {1.display_name}'.format(
                datetime.strptime(x['date'], DATE_BACK).strftime('%B %-d'),
                id_resolver(x['id'])
            )
            for x in dict(bdays).values()
        ]

    @commands.command()
    @is_admin()
    async def bdaychan(self, context, *, channel: discord.TextChannel=None):
        target = channel or context.channel
        #TODO verify channel is in server
        with self.bot.db() as db:
            db.set('servers', context.guild.id, {'birthday_channel': target.id})
            db.commit()
        await context.send('Set {} to the birthday channel of this server da-don~'.format(target))

    @commands.command()
    @commands.guild_only()
    async def bdays(self, context, n: int = 5):
        with self.bot.db() as db:
            entries = db.get('birthdays', [m.id for m in context.guild.members])
            today_power = self.to_power(datetime.now().strftime(DATE_BACK))
            ranking = {}
            for e in entries:
                relative_power = self.to_power(e['date']) - today_power
                if relative_power < 0:
                    relative_power += 1212
                ranking[relative_power] = e
            ranking = sorted(ranking.items())[:n]
            msg = listify(self.to_bdays_list(ranking, context.guild.get_member))
            await context.send(embed=MechaEmbed(
                title='Upcoming birthdays',
                description=msg,
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
