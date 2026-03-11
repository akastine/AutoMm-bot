import discord
from discord.ui import TextInput, Modal
from function import *

class walletModal(Modal):
    def __init__(self, prvKey, amount, crypto_type="LTC"):
        self.prvKey = prvKey
        self.amount = amount
        self.crypto_type = crypto_type
        crypto_name = {"LTC": "Litecoin", "SOL": "Solana", "USDT": "USDT Polygon"}.get(crypto_type, "Litecoin")
        super().__init__(
            title=f"{crypto_name} Address"
        )

        placeholder_addresses = {
            "LTC": "LVeJaGL2evHhgFCVa6GQWamL18oCdwLb2c",
            "SOL": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
            "USDT": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        }

        wallet = TextInput(
            label="Your Wallet",
            placeholder=f"Example: {placeholder_addresses.get(crypto_type, placeholder_addresses['LTC'])}",
            required=True,
            style=discord.TextStyle.short,
            min_length=1
        )

        self.add_item(wallet)

    async def on_submit(self, interaction: discord.Interaction):
        toAddress = self.children[0].value
        txId = send_to_address(self.prvKey, toAddress, self.crypto_type)
        crypto_name = {"LTC": "Litecoin", "SOL": "Solana", "USDT": "USDT Polygon"}.get(self.crypto_type, "Litecoin")
        embed = discord.Embed(
            title="MiddleMan Confirmed",
            description=f"""
# The deal processed successfully, now please wait...

> **Cryptocurrency:** `{crypto_name}`
> **Transaction Id:** `{txId}`
> **Wallet:** `{toAddress}`
> **Amount:** `{self.amount} €`

**Please double check your wallet when you received and you confirm this transaction.**
            """,
            color=embed_color()
        )
        await interaction.response.edit_message(embed=embed, view=None, content=None)
        