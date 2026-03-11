import json
import discord
from discord.ui import Button
from function import *
import asyncio
from .copyAddress import copyAddress
from .confirmDeal import confirmDeal
from .refundButton import refundButton

class confirmRoles(Button):
    def __init__(self, filename):
        self.filename = filename
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Confirm",
            emoji="✅"
        )
        
    async def callback(self, interaction: discord.Interaction):
        file = json.load(open(f"process/{self.filename}.json", 'r'))
        if interaction.user.id == file['sender']:
            if file['senderConfirm'] == True:
                return await interaction.response.send_message("You already confirmed this roles, please wait the second user confirmation.", ephemeral=True)
                
            file['senderConfirm'] = True
            file['rolesConfirm'] = file['rolesConfirm'] + 1
            json.dump(file, open(f"process/{self.filename}.json", 'w'), indent=4)
        elif interaction.user.id == file['recever']:
            if file['receverConfirm'] == True:
                return await interaction.response.send_message("You already confirmed this roles, please wait the second user confirmation.", ephemeral=True)
            file['receverConfirm'] = True
            file['rolesConfirm'] = file['rolesConfirm'] + 1
            json.dump(file, open(f"process/{self.filename}.json", 'w'), indent=4)
            
        file = json.load(open(f"process/{self.filename}.json", 'r'))
        senderConfirmation = "✅" if file['senderConfirm'] == True else "❌"
        receverConfirmation = "✅" if file['receverConfirm'] == True else "❌"
        embed = discord.Embed(
            title="Roles Confirmations...",
            description=f"Are you sure you take rights roles \n\n> **Sender Confirmation: {senderConfirmation}**\n> **Recever Confirmation: {receverConfirmation}**",
            color=embed_color()
        )
        embed.add_field(name="Sender Confirmation", value=f"<@{file['sender']}>", inline=True)
        embed.add_field(name="Recever", value=f"<@{file['recever']}>", inline=True)
        embed.set_footer(text=f"[{file['rolesConfirm']}/2] Confirmed")
        await interaction.response.edit_message(view=self.view, embed=embed)
        if file['rolesConfirm'] == 2:
            crypto_type = file.get('crypto_type', 'LTC')
            wallet, privateKey, publicKey, wif = create_wallet(crypto_type)
            crypto_name = {"LTC": "Litecoin", "SOL": "Solana", "USDT": "USDT Polygon"}.get(crypto_type, "Litecoin")
            embed = discord.Embed(
                title="Awaiting Payment",
                description=f"""
# <@{file['sender']}> Please send amount at this address:

> **Cryptocurrency:** `{crypto_name}`
> **Address:** `{wallet}`
> **Please send only {crypto_name} and no other cryptocurrency.**
                """,
                color=embed_color()
            )
            embed.set_footer(text="Awaiting payment... [Anything]")
            view = discord.ui.View(timeout=None)
            view.add_item(copyAddress(wallet, self.filename))
            await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)
            time = 0
            while True:
                check, amount_raw = check_transactions(wallet, crypto_type)
                if check == "detected but not confirmed":
                    embed = discord.Embed(
                        title="Payment Detected",
                        description=f"""
# Payment detected, please wait confirmation:

> **Cryptocurrency:** `{crypto_name}`
> **Address:** `{wallet}`
> **Please send only {crypto_name} and no other cryptocurrency.**
                        """, color=embed_color()
                    )
                    embed.set_footer(text="Detected payment... [Detected]")
                    await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=None)
                elif check == "confirmed":
                    try:
                        if crypto_type == "LTC":
                            cryptoAmount = amount_raw / 100000000
                            crypto_unit = "LTC"
                        elif crypto_type == "SOL":
                            cryptoAmount = amount_raw / 1000000000
                            crypto_unit = "SOL"
                        elif crypto_type == "USDT":
                            cryptoAmount = amount_raw / 1000000
                            crypto_unit = "USDT"
                        else:
                            cryptoAmount = amount_raw
                            crypto_unit = crypto_type

                        eurAmount = convertToFiat(cryptoAmount, crypto_type)
                        embed = discord.Embed(
                            title="Payment Confirmed and Received",
                            description=f"""
# Payment confirmed and received.

> **Amount in {crypto_name}:** `{cryptoAmount} {crypto_unit}`
> **Amount in €:** `{eurAmount} €`
> **Now you can process to exchange**
> **Please confirm the deal after you get your products**
                            """,
                            color=embed_color()
                        )
                        embed.set_footer(text="Received payment [Waiting]")
                        view = discord.ui.View(timeout=None)
                        view.add_item(confirmDeal(self.filename, privateKey, eurAmount, crypto_type))
                        view.add_item(refundButton(self.filename, eurAmount, privateKey, crypto_type))
                        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)
                        config = load_json()
                        logsConfig = config['config']['logs']
                        if logsConfig['status'] == "on":
                            if logsConfig['channel'] != None:
                                file = json.load(open(f"process/{self.filename}.json", 'r'))
                                senderId = file['sender']
                                receverId = file['recever']
                                logsChannel = discord.utils.get(interaction.guild.channels, id=logsConfig['channel'])
                                if logsChannel:
                                    embed = discord.Embed(
                                        title="`✨`・Deal completed",
                                        description=f"*A middleman deal finished now.*",
                                        color=embed_color()
                                    )
                                    embed.add_field(name="Sender Infos", value=f"> **Id:** {senderId}\n> **Mention:** <@{senderId}>\n> **Role:** Sender")
                                    embed.add_field(name="Recever Infos", value=f"> **Id:** {receverId}\n> **Mention:** <@{receverId}>\n> **Role:** Sender")
                                    embed.set_footer(text=footer(self.bot, uid=self.filename))
                                    await logsChannel.send(embed=embed)
                        break
                    except Exception as e:
                        print(e)
                await asyncio.sleep(90)
                time += 0.5