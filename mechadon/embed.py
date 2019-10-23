from discord import Embed

class MechaEmbed(Embed):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if 'context' in kwargs:
            text = '{0.cog.qualified_name} / {0.command.name}'.format(kwargs['context'])
        else:
            text = ''
        icon_url = 'https://cdn.discordapp.com/emojis/477980675434348554.png?v=1'
        self.set_footer(text=text, icon_url=icon_url)

    def add_fields(self, fields):
        for field in fields:
            self.add_field(**field)
