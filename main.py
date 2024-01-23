import discord
import os
import sys
from discord.ext import commands
from os.path import join, dirname
from dotenv import load_dotenv


class role_manager(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=intents,
            help_command=None,
            command_prefix='h!'
        )
        self.initial_extensions = [
            "cogs.memberize",
            "cogs.visitorize"
        ]
    
    async def setup_hook(self):
        for extension in self.initial_extensions:
            await self.load_extension(extension)
    
    async def on_ready(self):
        print("get on ready!")
        sys.stdout.flush()
        return

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

token = os.environ.get("TOKEN")
guild_id = int(os.environ.get("GUILD_ID"))
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = role_manager()
bot.run(token)