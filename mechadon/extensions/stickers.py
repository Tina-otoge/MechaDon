import aiohttp
import io
import json
import os
import pathlib

import discord
from discord.ext import commands

from .string import listify
from mechadon.embed import MechaEmbed

def get_filename(path, name=None):
    path = pathlib.Path(path)
    name = name or path.stem
    return name + path.suffix

class Stickers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.path = 'stickers.json'
        self.session = aiohttp.ClientSession(loop=bot.loop)
        try:
            with open(self.path) as f:
                self.stickers = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.initialize_stickers()

    def initialize_stickers(self):
        self.stickers = {}
        self.save()

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.stickers, f)

    @commands.command()
    async def stickers(self, context):
        await context.send(embed=MechaEmbed(
            title='List of trigger words to send a sticker',
            description=listify(self.stickers.keys()),
            context=context
        ))

    @commands.command()
    @commands.is_owner()
    async def sticker(self, context, name: str):
        if len(context.message.attachments) == 0:
            if name not in self.stickers:
                raise KeyError('{} is not a sticker!'.format(name))
            self.stickers.pop(name)
            action = 'Removed'
        else:
            action = 'Updated' if name in self.stickers else 'Added'
            self.stickers[name] = context.message.attachments[0].url
            context.trigger_typing()
        self.save()
        await context.send('{} sticker {} da-don~!'.format(action, name))

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content.strip().casefold()
        stickers_url = self.stickers.get(content, None)
        if stickers_url:
            async with message.channel.typing():
                async with self.session.get(stickers_url) as response:
                    fp = io.BytesIO(await response.read())
                    await message.channel.send(file=discord.File(
                        fp,
                        filename=get_filename(stickers_url, content)
                    ))
