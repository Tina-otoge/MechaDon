import discord

class ErrorHandler:

    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, exception, context):
        embed = self.bot.create_embed(context=context)

        embed.title       = '*Dongyaa--!!*'
        embed.colour      = discord.Colour.orange()
        embed.description = str(exception)

        await self.bot.send_message(context.message.channel, embed=embed)

