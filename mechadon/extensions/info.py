import discord
from discord.ext import commands

from .time import TIME_FRONT
from mechadon.embed import MechaEmbed

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def joined(self, context, *, member: discord.Member = None):
        target = member or context.author
        await context.send('{0.display_name} joined {0.guild} on {1}'.format(
            target, target.joined_at.strftime(TIME_FRONT)
        ))

    @commands.command()
    async def created(self, context, *, user: discord.User = None):
        target = user or context.author
        await context.send(
            '{0.display_name}\'s account was created on {1}'.format(
                target, target.created_at.strftime(TIME_FRONT)
            )
        )

    @commands.command()
    @commands.guild_only()
    async def topic(self, context, *, channel: discord.TextChannel = None):
        target = channel or context.message.channel
        if target.topic is None:
            await context.send(
                'Sorry da-don... There is no topic set on this channel...'
                '\n(´；ω；`)'
            )
            return
        content = target.topic
        if target != context.message.channel:
            content += '\n\nLink: {0.mention}'.format(target)
        await context.send(embed=MechaEmbed(
            title='#{}\'s topic'.format(target),
            description=content,
            context=context
        ))
