import json
import discord
from discord import app_commands
from discord.ext import commands
from function import load_json, unauthorized, embed_color

class setDevRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup-developer-role", description="Set the developer role for fund release commands")
    async def setupdevrole(self, interaction: discord.Interaction, role: discord.Role):
        config = load_json()
        if interaction.user.id != config['buyer']:
            return await unauthorized(interaction)

        config['developer_role_id'] = role.id
        json.dump(config, open("config.json", 'w'), indent=4)
        embed = discord.Embed(
            title="`✅`・Developer Role",
            description=f"*The role {role.mention}`{role.id}` has been set as the developer role.*",
            color=embed_color()
        )
        embed.set_footer(text=config['footer'])
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(setDevRole(bot))
