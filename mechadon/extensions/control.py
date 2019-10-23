from discord.ext import commands

class Control(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def kill(self, context):
        await context.send('😉🔫')
        await self.bot.close()
