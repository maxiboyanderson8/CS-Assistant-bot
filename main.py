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
import os
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
        embed.add_field(name="**<:CD_dot:1310207495691567145> Rating:**", value="".join(["<:CD_Star:1337489151154454529>"] * rating), inline=True)
        embed.add_field(name="**<:CD_dot:1310207495691567145> Extra Notes:**", value=extra_notes, inline=False)
        embed.set_footer(text="Thank you for your review", icon_url="https://media.discordapp.net/attachments/1307830343482478725/1307837864914059314/CDLOGO_MGMT_BLACK.png?ex=674c3d2d&is=674aebad&hm=f3b757b37d41bcb9d68f8c408fe55c800b84cb6e3b6bd841a118045435bc51da&=&format=webp&quality=lossless&width=481&height=481")
        embed.timestamp = interaction.created_at

        review_channel = client.get_channel(REVIEWS_ID)
        if review_channel:
            await review_channel.send(designer.mention)
            await review_channel.send(embed=embed)
            await interaction.response.send_message("Review submitted successfully!", ephemeral=True)
        else:
            await interaction.response.send_message("Review channel not found.", ephemeral=True)
    except Exception as e:
        logging.error(f"Error in review command: {e}")
        await interaction.response.send_message("An error occurred while submitting your review.", ephemeral=True)

# ORDER LOG SLASH COMMAND --------------------------------------------------------------------------------
@client.slash_command(guild_ids=[GUILD_ID], description="Use this command to log your order")
async def order_log(
    interaction: Interaction,
    designer: nextcord.Member = SlashOption(description="Designer to log", required=True),
    original_price: float = SlashOption(description="Price without tax", required=True),
    total_price: float = SlashOption(description="Price including tax", required=True),
    ticket_id: str = SlashOption(description="Ticket ID", required=True),
    note: str = SlashOption(description="Additional notes", required=False, default="No additional notes provided.")
):
    try:
        # Check if the user invoking the command has the correct role
        if "Staff Team" not in [role.name for role in interaction.user.roles]:
            await interaction.response.send_message("❌ You don't have the required role to log orders.", ephemeral=True)
            return

        # Check if the designer has the required role
        if "Creative Team" not in [role.name for role in designer.roles]:
            await interaction.response.send_message("❌ The designer must have the 'Creative Team' role to be logged.", ephemeral=True)
            return

        if original_price > total_price:
            await interaction.response.send_message("❌ Original price must be less than or equal to total price.", ephemeral=True)
            return

        embed = nextcord.Embed(title="<:CD_cart:1322299968450461737> Order Log", color=0xff913a)
        embed.set_image(url="https://media.discordapp.net/attachments/1110779991626629252/1312520876239097876/Sin_titulo_72_x_9_in_72_x_5_in_1_1.png?ex=674ccbd2&is=674b7a52&hm=f6228f89e71982bdbcd236455249a0f0fba8796855434204803f0d108e8c7157&=&format=webp&quality=lossless&width=1439&height=100")
        embed.add_field(name="<:CD_Discord:1310206398717755532> Designer", value=designer.mention, inline=False)
        embed.add_field(name="<:CD_robux:1310207300522213507> Original Price", value=f"${original_price:.2f}", inline=True)
        embed.add_field(name="<:CD_robux:1310207300522213507> Total Price", value=f"${total_price:.2f}", inline=True)
        embed.add_field(name="<:CD_settings:1310207018161934376> Ticket ID", value=ticket_id, inline=True)
        embed.add_field(name="<:CD_dot:1310207495691567145> Note", value=note, inline=False)
        embed.set_footer(text=f"Logged by {interaction.user}", icon_url=interaction.user.avatar.url)
        
        log_channel = client.get_channel(ORDER_LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(content=f"{designer.mention}", embed=embed)
            await interaction.response.send_message("✅ Order log successful.", ephemeral=True)
            
            # Update order logs
            if designer.name not in order_logs:
                order_logs[designer.name] = {
                    "total_logs": 0,
                    "total_earnings": 0.0
                }
            order_logs[designer.name]["total_logs"] += 1
            order_logs[designer.name]["total_earnings"] += original_price
            
            # Update permanent order logs
            if designer.name not in perm_order_logs:
                perm_order_logs[designer.name] = {
                    "total_logs": 0,
                    "total_earnings": 0.0
                }
            perm_order_logs[designer.name]["total_logs"] += 1
            perm_order_logs[designer.name]["total_earnings"] += original_price
            
            # Save order logs to file
            save_order_logs()
        else:
            await interaction.response.send_message("⚠️ Log channel not found.", ephemeral=True)
    except Exception as e:
        logging.error(f"Error in order_log command: {e}")
        await interaction.response.send_message("❌ An error occurred while logging the order.", ephemeral=True)

# SUPPORT LOG SLASH COMMAND --------------------------------------------------------------------------------
@client.slash_command(guild_ids=[GUILD_ID], description="Use this command to log your support ticket")
async def support_log(
    interaction: Interaction,
    support_staff: nextcord.Member = SlashOption(description="Support staff to log", required=True),
    date_of_opening: str = SlashOption(description="Date of opening", required=True),
    date_of_closing: str = SlashOption(description="Date of closing", required=True),
    ticket_id: str = SlashOption(description="Ticket ID", required=True),
    note: str = SlashOption(description="Additional notes", required=False, default="N/A")
):
    try:
        # Check if the invoker has the correct role
        if not any(role.name in ["Support Team", "Board of Directors", "Executive Board"] for role in interaction.user.roles):
            await interaction.response.send_message("❌ You don't have the required role to log support tickets.", ephemeral=True)
            return

        # Check if the target support staff has the Support Team role
        if "Support Team" not in [role.name for role in support_staff.roles]:
            await interaction.response.send_message("❌ The support staff must have the 'Support Team' role to be logged.", ephemeral=True)
            return

        # Create the embed
        embed = nextcord.Embed(title="<:CD_Info:1310206627466711140> Support Log", color=0xff913a)
        embed.set_image(url="https://media.discordapp.net/attachments/1110779991626629252/1312520876239097876/Sin_titulo_72_x_9_in_72_x_5_in_1_1.png?ex=674ccbd2&is=674b7a52&hm=f6228f89e71982bdbcd236455249a0f0fba8796855434204803f0d
        
