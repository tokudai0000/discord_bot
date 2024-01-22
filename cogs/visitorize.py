import discord
import os
from discord import app_commands
from discord.ext import commands
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
guild_id = int(os.environ.get("GUILD_ID"))
member_role_id=int(os.environ.get("MEMBER_ID"))
visitor_role_id=int(os.environ.get("VISITOR_ID"))
random_category_id=int(os.environ.get("CATEGORY_ID"))

#ユーザが加入した際にビジターロールを付与する
class visitorize(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        guild = self.bot.get_guild(guild_id)
        visitor_role = guild.get_role(visitor_role_id)
        await member.add_roles(visitor_role)

async def setup(bot: commands.Bot):
    await bot.add_cog(
    visitorize(bot)
    )