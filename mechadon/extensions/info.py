import discord
from discord.ext import commands

from .time import TIME_FRONT

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
