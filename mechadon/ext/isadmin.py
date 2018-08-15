from discord.ext import commands

def is_admin(context):
    author = context.message.author
    server = context.message.server

    with context.bot.db_interface() as db:
        for row in db.get_by_id('bot_admins', author.id):
            if row['server_id'] is None or row['server_id'] == server.id:
                return True

    raise commands.errors.CheckFailure('this command can only be invoked by an admin')
