import discord
from discord.ui import View, Button
from .startModal import startModal

class CryptoSelectView(View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

        ltc_button = Button(
            style=discord.ButtonStyle.secondary,
            label="Litecoin (LTC)",
            custom_id="crypto_ltc"
        )
        ltc_button.callback = self.ltc_callback

        sol_button = Button(
            style=discord.ButtonStyle.secondary,
            label="Solana (SOL)",
            custom_id="crypto_sol"
        )
        sol_button.callback = self.sol_callback

        usdt_button = Button(
            style=discord.ButtonStyle.secondary,
            label="USDT Polygon",
            custom_id="crypto_usdt"
        )
        usdt_button.callback = self.usdt_callback

        self.add_item(ltc_button)
        self.add_item(sol_button)
        self.add_item(usdt_button)

    async def ltc_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(startModal(interaction.user.id, self.bot, "LTC"))

    async def sol_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(startModal(interaction.user.id, self.bot, "SOL"))

    async def usdt_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(startModal(interaction.user.id, self.bot, "USDT"))
