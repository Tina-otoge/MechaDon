from discord import Embed

class MechaEmbed(Embed):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if 'context' in kwargs:
            text = kwargs.get('context').invoked_with
        else:
            text = None
        icon_url = 'http://skiel.pro/apps/MechaDon/icon.png'
        self.set_footer(text=text, icon_url=icon_url)

    def add_fields(self, fields):
        for field in fields:
            self.add_field(**field)
