import discord
from function import *
from discord import app_commands
from discord.ext import commands
from view.startButton import startButton
from function import unauthorized

class MiddleManEmbed(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @app_commands.command(name="middleman-embed", description="Send MiddleMan Panel")
    async def mmembed(self, interaction: discord.Interaction) -> None:
        config = load_json()
        if interaction.user.id not in config['whitelist'] and interaction.user.id != config['buyer']:
            return await unauthorized(interaction)
        embed = discord.Embed(
            title="Rainy MM & Exch",
            description="Rainymm Escrow makes your cryptocurrency trades safe and easy. We provide a secure environment for peer-to-peer deals, protecting you from fraud and scams.\n\n**How this works?**\n\nOur automated system handles everything. Funds are only released when both parties are satisfied, ensuring a fair and reliable experience for every user.\n\nSelect an asset below to start your deal.",
            color=embed_color()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(startButton(self.bot))
        await interaction.response.send_message(embed=embed, view=view)
        
async def setup(bot) -> None:
    await bot.add_cog(MiddleManEmbed(bot))