import discord
from discord.ext import commands

def is_admin():
    def predicate(context):
        author = context.message.author
        server = context.message.guild

        with context.bot.db() as db:
            for row in db.get('bot_admins', author.id):
                if row['server_id'] is None or row['server_id'] == server.id:
                    return True
        raise commands.errors.CheckFailure('this command can only be invoked by an admin')
    return commands.check(predicate)

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='op')
    @commands.is_owner()
    async def set_admin(self, context, user:  discord.User, scope: str = None):
        if scope is not None and scope != 'everywhere':
            raise commands.errors.BadArgument(
                'Scope has to be "everywhere" or nothing at all'
            )
        server = None if scope == 'everywhere' else context.guild
        data = {'id': user.id, 'server_id': server.id if server else None}
        scope_msg = 'for the scope of this server' if server else 'everywhere'
        with self.bot.db() as db:
            if len(db.get('bot_admins', data)) > 0:
                db.delete('bot_admins', data)
                await context.send('{} is no longer an admin {}'.format(
                        user,
                        scope_msg
                ))
            else:
                db.insert('bot_admins', data)
                await context.send('{} is now an admin {}'.format(
                    user,
                    scope_msg
                ))
            db.commit()

