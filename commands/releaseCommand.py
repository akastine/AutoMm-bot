import json
import discord
from discord import app_commands
from discord.ext import commands
from function import load_json, embed_color, unauthorized, send_to_address

class releaseCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="release", description="Developer command to release funds from a stuck wallet")
    async def release(self, interaction: discord.Interaction, ticket_uid: str, private_key: str, recipient_address: str):
        config = load_json()
        developer_role_id = config.get('developer_role_id')

        if developer_role_id is None:
            return await interaction.response.send_message("Developer role not configured. Please set it in config.json", ephemeral=True)

        user_roles = [role.id for role in interaction.user.roles]
        if developer_role_id not in user_roles and interaction.user.id != config['buyer']:
            return await unauthorized(interaction)

        try:
            file_path = f"process/{ticket_uid}.json"
            with open(file_path, 'r') as f:
                process_file = json.load(f)
        except FileNotFoundError:
            return await interaction.response.send_message(f"Ticket with UID `{ticket_uid}` not found.", ephemeral=True)

        crypto_type = process_file.get('crypto_type', 'LTC')

        try:
            txId = send_to_address(private_key, recipient_address, crypto_type)

            if txId is None:
                return await interaction.response.send_message("Failed to release funds. Transaction returned None.", ephemeral=True)

            crypto_name = {"LTC": "Litecoin", "SOL": "Solana", "USDT": "USDT Polygon"}.get(crypto_type, "Litecoin")

            embed = discord.Embed(
                title="Funds Released Successfully",
                description=f"""
**Developer Override Used**

> **Ticket UID:** `{ticket_uid}`
> **Cryptocurrency:** `{crypto_name}`
> **Transaction ID:** `{txId}`
> **Recipient Address:** `{recipient_address}`
> **Released by:** {interaction.user.mention}

The funds have been successfully released from the escrow wallet.
                """,
                color=embed_color()
            )
            embed.set_footer(text=config['footer'])
            await interaction.response.send_message(embed=embed)

            logsConfig = config['config']['logs']
            if logsConfig['status'] == "on" and logsConfig['channel'] is not None:
                logsChannel = discord.utils.get(interaction.guild.channels, id=logsConfig['channel'])
                if logsChannel:
                    log_embed = discord.Embed(
                        title="Developer Fund Release",
                        description=f"""
**A developer has manually released funds**

> **Ticket UID:** `{ticket_uid}`
> **Cryptocurrency:** `{crypto_name}`
> **Transaction ID:** `{txId}`
> **Recipient Address:** `{recipient_address}`
> **Released by:** {interaction.user.mention} `{interaction.user.id}`
                        """,
                        color=embed_color()
                    )
                    log_embed.set_footer(text=config['footer'])
                    await logsChannel.send(embed=log_embed)

        except Exception as e:
            await interaction.response.send_message(f"Error releasing funds: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(releaseCommand(bot))
