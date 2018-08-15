import discord
from discord.ext import commands

class SelfRoles:

    def __init__(self, bot):
        self.bot = bot

    async def toggle_role(bot, user, role):
        if role in user.roles:
            await bot.remove_roles(user, role)
        else:
            await bot.add_roles(user, role)

    @commands.command(pass_context=True, no_pm=True, aliases=['register'])
    async def role(self, context, *, asked_role : str):

        asked_role = asked_role.casefold()
        server_roles = context.message.server.roles
        found = None
        for role in server_roles:
            if str(role).casefold() == asked_role:
                found = role
                break
        if not found:
            raise Exception('The asked role does not exist on this server')

        try:
            toggle_role(self.bot, conext.message.author, found)
        except discord.errors.CommandInvokeError as e:
            if e.status == 403:
                raise Exception('The asked role is not self-assignable')
            else:
                raise e
