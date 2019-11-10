import discord
from discord.ext import commands

from mechadon.embed import MechaEmbed
from .admin import is_admin
from .string import listify

class SelfRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def complain_not_exists(self, role):
        raise KeyError('The role {} does not exist on this server'.format(name))

    @commands.command(name='role')
    @commands.guild_only()
    async def set(self, context, *, role: discord.Role):
        server     = context.message.guild
        user       = context.message.author
        if role not in server.roles:
            self.complain_not_exists(role)
        with self.bot.db() as db:
            if len(db.get('selfroles', role.id)) == 0:
                raise Exception('The role {} is not self-assignable'.format(
                    role))
        if role not in user.roles:
            await user.add_roles(role)
            fmt = 'I added you the {} role da-don~'
        else:
            await user.remove_roles(role)
            fmt = 'as you requested, you no longer have the {} role da-don...'
        await context.send(fmt.format(role))

    @commands.command(name='roles')
    @commands.guild_only()
    async def list(self, context):
        server = context.message.guild
        roles  = []
        with self.bot.db() as db:
            for row in db.get('selfroles', {'server_id': server.id}):
                role = server.get_role(row['id'])
                if role is not None:
                    roles.append(role)
        await context.send(embed=MechaEmbed(
            title='Self-assignable roles',
            description=listify(roles),
            context=context
        ))

    @commands.command(name='roletoggle')
    @commands.guild_only()
    @is_admin()
    async def toggle(self, context, *, role: discord.Role):
        server     = context.message.guild
        if role not in server.roles:
            self.complain_not_exists(role)
        with self.bot.db() as db:
            if len(db.get('selfroles', role.id)) > 0:
                db.delete('selfroles', role.id)
                fmt = 'Removed {} from selfroles'
            else:
                db.insert('selfroles', {'id': role.id, 'server_id': server.id})
                fmt = 'Added {} to selfroles'
            db.commit()

        await context.send(fmt.format(role))

    @commands.command(name='rolesclean')
    @is_admin()
    async def clean(self, context):
        server = context.message.guild
        server_roles_by_id     = []
        selfrole_ids_to_remove = []

        for role in server.roles:
            server_roles_by_id.append(role.id)

        with self.bot.db() as db:
            selfrole_rows = db.get('selfroles', {'server_id': server.id})

            for row in selfrole_rows:
                if row['id'] not in server_roles_by_id:
                    selfrole_ids_to_remove.append(selfrole_id)
            removed_roles_count = len(selfrole_ids_to_remove)

            for selfrole_id in selfrole_ids_to_remove:
                db.delete('selfroles', selfrole_id)
            if removed_roles_count > 0:
                db.commit()
        await context.send('Removed {} unused roles'.format(removed_roles_count))
