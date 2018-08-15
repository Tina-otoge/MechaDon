import discord
from discord.ext import commands

from .isadmin import is_admin

def _get_role(server, role):
    predicate    = lambda r: r.name.casefold() == role.casefold()
    result       = discord.utils.find(predicate, server.roles)

    if result is None:
        raise Exception('The role {} does not exist on this server'.format(
            role))

    return result

class SelfRoles:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True, aliases=['register'])
    async def role(self, context, *, role : str):
        server     = context.message.server
        user       = context.message.author
        asked_role = _get_role(server, role)
        
        with self.bot.db_interface() as db:
            if len(db.get_by_id('selfroles', asked_role.id)) == 0:
                raise Exception('The role {} is not self-assignable'.format(
                    role))
        
        if asked_role not in user.roles:
            await self.bot.add_roles(user, asked_role)
            fmt = 'I added you the {} role da-don~'
        else:
            await self.bot.remove_roles(user, asked_role)
            fmt = 'as you requested, you no longer have the {} role da-don...'
        
        await self.bot.reply(fmt.format(asked_role))

    @commands.command(pass_context=True, no_pm=True)
    async def selfroleslist(self, context):
        server = context.message.server
        roles  = []

        with self.bot.db_interface() as db:
            for row in db.get_by('selfroles', {'server_id': server.id}):
                role = discord.utils.find(lambda r: r.id == row['id'], server.roles)
                if role is not None:
                    roles.append(role)

        embed = self.bot.create_embed(context=context)
        embed.title = 'Self-assignable roles'
        embed.description = '\n'.join(r.name for r in roles)
        await self.bot.send_message(context.message.channel, embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def selfroletoggle(self, context, *, role : str):
        is_admin(context)
        server     = context.message.server
        asked_role = _get_role(server, role)

        with self.bot.db_interface() as db:
            if len(db.get_by_id('selfroles', asked_role.id)) > 0:
                db.delete_by_id('selfroles', asked_role.id)
                fmt = 'removed {} from selfroles'
            else:
                db.insert('selfroles', asked_role.id, {'server_id': server.id})
                fmt = 'added {} to selfroles'
            db.commit()

        await self.bot.reply(fmt.format(asked_role))

    @commands.command(pass_context=True, no_pm=True)
    async def selfrolesclean(self, context):
        is_admin(context)
        server = context.message.server
        server_roles_by_id     = []
        selfrole_ids_to_remove = []

        for role in server.roles:
            server_roles_by_id.append(role.id)

        with self.bot.db_interface() as db:
            selfrole_rows = db.get_by('selfroles', {'server_id': server.id})

            for row in selfrole_rows:
                if row['id'] not in server_roles_by_id:
                    selfrole_ids_to_remove.append(selfrole_id)
            removed_roles_count = len(selfrole_ids_to_remove)

            for selfrole_id in selfrole_ids_to_remove:
                db.delete_by_id('selfroles', selfrole_id)
            if removed_roles_count > 0:
                db.commit()

        await self.bot.reply('removed {} unused roles'.format(removed_roles_count))
