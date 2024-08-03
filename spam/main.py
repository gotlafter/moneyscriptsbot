import discord
from discord.ext import commands
import asyncio
import json
import sys

intents = discord.Intents.default()
intents.messages = True

async def create_client(token, channel_id, message):
    client = commands.Bot(command_prefix='*', intents=intents)

    @client.event
    async def on_ready():
        print(f"Account with token {token} is online")
        channel = client.get_channel(channel_id)
        
        if channel:
            while True:
                try:
                    await channel.send(message)
                    await asyncio.sleep(0.1)
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        print("Rate limited. Waiting for 30 seconds.")
                        await asyncio.sleep(30)
                    else:
                        print(f"An error occurred: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
        else:
            print(f"Channel with ID {channel_id} not found.")

    await client.start(token, bot=False)

async def main(tokens_file):
    with open(tokens_file) as f:
        data = json.load(f)
        tokens = data.get('tokens', [])

    channel_id = int(input("Enter the channel ID: "))
    message = input("Enter the message to send: ")
    
    await asyncio.gather(*[create_client(token, channel_id, message) for token in tokens])

if __name__ == "__main__":
    try:
        tokens_file = 'tokens.config'
        asyncio.run(main(tokens_file))
    except KeyboardInterrupt:
        print("shutting down gracefully...")
        sys.exit(0)