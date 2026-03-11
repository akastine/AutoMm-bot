# Discord Auto-MiddleMan Bot
The most secure discord auto middleman bot for your discord market server with multi-cryptocurrency support

## Table Of Content

✨ [Installation](#install) <br/>
🧪 [Configuration](#config)<br/>
📍 [Starting](#start)<br/>


## Installation
<div id="install"></div>

Clone the repository:
```
git clone https://github.com/Celentroft/AutoMm-bot.git
```
Install requirements:
```
pip install -r requirements.txt
```
(Don't forget to install python !)

## Configuration
<div id="config"></div>

After the installation you need to configure the `config.json` file
```json
{
    "developer": "scarlxrd1337", -> Dont be a skid lmao
    "token": "token", -> Your bot token
    "buyer": null, -> Your discord Id
    "developer_role_id": null, -> Developer role ID for /release command
    "color": "hex_color", -> Embeds Colors (Hex Code)
    "footer": "Your footer", -> Embeds Footer (strings)
    "blockcypher": "blockcypher api key", -> Blockcypher API key for Litecoin
    "solana_api_key": "solana api key", -> Solana API key (to be configured)
    "polygon_api_key": "polygon api key", -> Polygon API key for USDT (to be configured)
    "whitelist": [], -> Don't need to change (using with commands)
    "scammers": [], -> Useless
    "config": {
        "logs": {
            "status": "off",
            "channel": null
        },
        "tickets": {
            "category": null
        }
    }
}
```

## Features

- Multi-cryptocurrency support: Litecoin (LTC), Solana (SOL), and USDT Polygon
- Automatic escrow system
- Secure wallet generation
- Transaction monitoring and confirmation
- Developer override command for stuck funds
- Logging system for all transactions
- Role-based access control

## Starting
<div id="start"></div>

After the bot configuration, you need to run the bot :O
```
python main.py
```
And you may see a nice commands output logs !


## Please star this repository !