import discord
from discord.ext import commands
from discord.utils import get
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN = config['TOKEN']
GUILD_ID = config['GUILD_ID']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await main()

async def get_or_create_channel(guild, channel_name, category_id=None):
    channel = get(guild.channels, name=channel_name)
    if channel is None:
        print(f"Creating channel {channel_name}")
        category = None
        if category_id:
            category = guild.get_channel(int(category_id))
            if not category or category.type != discord.ChannelType.category:
                print("Invalid category ID. Creating channel without category.")
                category = None
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(send_messages=False, view_channel=True)
        }
        channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
    return channel

async def main():
    guild = bot.get_guild(int(GUILD_ID))
    
    if guild is None:
        print(f"Guild with ID {GUILD_ID} not found. Ensure the bot is in the guild and the ID is correct.")
        return

    while True:
        existing_channel = input("Is there an existing channel? (yes/no): ").strip().lower()
        if existing_channel == 'yes':
            channel_id = int(input("Enter the channel ID: ").strip())
            channel = guild.get_channel(channel_id)
            if channel is None:
                print("Channel not found.")
                continue
        else:
            channel_name = input("Enter the name for the new channel: ").strip()
            category_choice = input("Do you want to put it in a category? (yes/no): ").strip().lower()
            category_id = None
            if category_choice == 'yes':
                category_id = input("Enter the category ID: ").strip()
            channel = await get_or_create_channel(guild, channel_name, category_id)

        script_name = input("Enter the name of the script: ").strip()
        script_content = input("Enter the script you want in the embed: ").strip()

        embed = discord.Embed(
            title=script_name,
            description=f"```lua\n-- {script_name}\n{script_content}\n```",
            color=5814783
        )

        await channel.send(embed=embed)

        another_script = input("Do you want to send another script? (yes/no): ").strip().lower()
        if another_script != 'yes':
            break

if __name__ == "__main__":
    bot.run(TOKEN)