import os
import discord
from discord.ext import commands
import asyncio

# -----------------------------
# Intents
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# -----------------------------
# Config
# -----------------------------
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable not set!")

WATCH_CHANNEL_ID = 1429648471518085171  # Replace with your channel ID
ROLE_ID = 1429643384129327164           # Replace with your role ID

# -----------------------------
# Events
# -----------------------------
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Watching channel ID: {WATCH_CHANNEL_ID} for role ID: {ROLE_ID}')

@bot.event
async def on_message(message):
    # Ignore bots
    if message.author.bot:
        return

    # Only watch a specific channel
    if message.channel.id != WATCH_CHANNEL_ID:
        return

    role = message.guild.get_role(ROLE_ID)
    if role is None:
        print(f"Role with ID {ROLE_ID} not found in guild {message.guild.name}!")
        return

    # Add role only if user doesn't already have it
    if role not in message.author.roles:
        try:
            await message.author.add_roles(role)
            print(f"Added role '{role.name}' to user {message.author}")
            # Optional: small delay to avoid hitting rate limits
            await asyncio.sleep(1)
        except discord.Forbidden:
            print(f"Missing permissions to add role '{role.name}' to {message.author}")
        except discord.HTTPException as e:
            print(f"HTTPException adding role: {e}")

    # Ensure commands still work
    await bot.process_commands(message)

# -----------------------------
# Run bot
# -----------------------------
bot.run(TOKEN)
