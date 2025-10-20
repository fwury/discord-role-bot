# pip install -U discord.py
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv("TOKEN")
WATCH_CHANNEL_ID = 1429648471518085171
ROLE_ID = 1429643384129327164

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != WATCH_CHANNEL_ID:
        return
    try:
        await message.author.add_roles(message.guild.get_role(ROLE_ID))
    except Exception as e:
        print('Error adding role:', e)

    await bot.process_commands(message)

bot.run(TOKEN)
