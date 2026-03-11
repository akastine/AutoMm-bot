import discord
from discord.ui import Button
from .cryptoSelectModal import CryptoSelectView
from function import embed_color

class startButton(Button):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__(
            style=discord.ButtonStyle.blurple,
            label="Select The Cryptocurrency",
            emoji="💎"
        )

    async def callback(self, interaction) -> None:
        embed = discord.Embed(
            title="Select The Cryptocurrency",
            description="Choose the cryptocurrency you want to use for this middleman transaction:",
            color=embed_color()
        )
        view = CryptoSelectView(self.bot)
        return await interaction.response.send_message(embed=embed, view=view, ephemeral=True)        