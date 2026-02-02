from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

import os
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Attachment, ButtonStyle
from nextcord.utils import get
import json
import nextcord
from nextcord.ext import commands
import logging
import requests
from nextcord.ui import Button, View, Modal, TextInput
import requests
from nextcord.utils import get
from apis import *
import random
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)

SUPPORTERS_ID = 1340663606848655450  # Replace with your supporters channel ID
GUILD_ID = 1337176811356028960
ORDER_LOG_CHANNEL_ID = 1337176812735692816  # Replace with your order logs channel ID
SUPPORT_LOG_CHANNEL_ID = 1467630775225548903  # Replace with your support logs channel ID
LOUNGE_ID = 1021619738306162690
REVIEWS_ID = 1337205475745464431  # Replace with your reviews channel ID
PROMOTION_ID = 1309857031087329391
INFRACTION_ID = 1309857105745936515

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='cd!', intents=intents)

# File to store order logs
ORDER_LOGS_FILE = 'order_logs.json'
SUPPORT_LOGS_FILE = 'support_logs.json'
LINKED_ACCOUNTS_FILE = 'linked_accounts.json'
# File to store permanent order logs
PERM_ORDER_LOGS_FILE = 'permorder_log.json'
PERM_SUPPORT_LOGS_FILE = 'permsupport_log.json'

# Load order logs from file
if os.path.exists(ORDER_LOGS_FILE):
    with open(ORDER_LOGS_FILE, 'r') as file:
        order_logs = json.load(file)
else:
    order_logs = {}

# Load support logs from file
if os.path.exists(SUPPORT_LOGS_FILE):
    with open(SUPPORT_LOGS_FILE, 'r') as file:
        support_logs = json.load(file)
else:
    support_logs = {}

# Load linked accounts from file
if os.path.exists(LINKED_ACCOUNTS_FILE):
    with open(LINKED_ACCOUNTS_FILE, 'r') as file:
        linked_accounts = json.load(file)
else:
    linked_accounts = {}

@client.event
async def on_ready():
    logging.info('Bot is ready.')
    logging.info('----------------------')

@client.event
async def on_member_join(member):
    logging.info(f"{member} has joined the server.")  
    guild = member.guild
    member_count = guild.member_count
    channel = nextcord.utils.get(guild.text_channels, id=LOUNGE_ID)
    if channel:
        await channel.send(f"<:CD_wave:1310206456712269876> Welcome to Comet Designs, {member.mention}! You are the `{member_count}` member. To place an order, please head over to <#1224486146046955590>. For more information, visit <#1021622027297239171>.")
    else:
        logging.warning("Channel not found. ----------------------")  

# Load permanent order logs from file
if os.path.exists(PERM_ORDER_LOGS_FILE):
    with open(PERM_ORDER_LOGS_FILE, 'r') as file:
        perm_order_logs = json.load(file)
else:
    perm_order_logs = {}

# Load permanent support logs from file
if os.path.exists(PERM_SUPPORT_LOGS_FILE):
    with open(PERM_SUPPORT_LOGS_FILE, 'r') as file:
        perm_support_logs = json.load(file)
else:
    perm_support_logs = {}

# Save order logs to file
def save_order_logs():
    with open(ORDER_LOGS_FILE, 'w') as file:
        json.dump(order_logs, file)
    with open(PERM_ORDER_LOGS_FILE, 'w') as file:
        json.dump(perm_order_logs, file)

# Save support logs to file
def save_support_logs():
    with open(SUPPORT_LOGS_FILE, 'w') as file:
        json.dump(support_logs, file)
    with open(PERM_SUPPORT_LOGS_FILE, 'w') as file:
        json.dump(perm_support_logs, file)

# Save linked accounts to file
def save_linked_accounts():
    with open(LINKED_ACCOUNTS_FILE, 'w') as file:
        json.dump(linked_accounts, file)

# REVIEW SLASH COMMAND --------------------------------------------------------------------------------
@client.slash_command(guild_ids=[GUILD_ID], description="Submit a review")
async def review(
    interaction: Interaction,
    designer: nextcord.Member = SlashOption(description="Designer to review, If you are unaware put comet designs as designer.", required=True, default="<@1088788105366097930>"),
    product: str = SlashOption(description="Name of the product", required=True),
    rating: int = SlashOption(description="Rating (1-5)", required=True, choices=[1, 2, 3, 4, 5]),
    extra_notes: str = SlashOption(description="Extra notes", required=False, default="No additional notes provided.")
):
    try:
        embed = nextcord.Embed(title="**<:CD_partner:1310207556903501844> Review**", color=0xff913a)
        embed.set_author(name=f"Review from {interaction.user}", icon_url=interaction.user.avatar.url)
        embed.set_image(url="https://media.discordapp.net/attachments/1110779991626629252/1312520876239097876/Sin_titulo_72_x_9_in_72_x_5_in_1_1.png?ex=674ccbd2&is=674b7a52&hm=f6228f89e71982bdbcd236455249a0f0fba8796855434204803f0d108e8c7157&=&format=webp&quality=lossless&width=1439&height=100")
        embed.add_field(name="**<:CD_dot:1310207495691567145> Designer:**", value=designer.mention, inline=True)
        embed.add_field(name="**<:CD_dot:1310207495691567145> Product:**", value=product, inline=True)
        embed.add_field(name="**<:CD_dot:1310207495691567145> Rating:**", value="".join(["<:CD_Star:1337489151154454529>"] *
        client.run(1392989220133408820)

