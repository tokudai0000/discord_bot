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

#指定されたユーザに個人randomチャンネルを作成し、メンバーロールを与える
class memberize(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        #tokenやidの取得
        self.guild: discord.Guild = self.bot.get_guild(guild_id)
        self.member_role: discord.Role = self.guild.get_role(member_role_id)
        self.visitor_role: discord.Role = self.guild.get_role(visitor_role_id)
        self.random_category:discord.TextChannel = self.guild.get_channel(random_category_id)

        await self.bot.tree.sync(guild=self.guild)

    @app_commands.command(
        name="memberize",
        description="指定されたユーザに個人用randomチャンネルを作成してメンバーロールを与えます。"
    )
    @app_commands.guilds(guild_id)
    async def memberize(self, ctx: discord.Interaction, user: discord.Member):
        if not(self.member_role in user.roles):  #ユーザがメンバーロールをもっていない場合のみ発火
            await self.guild.create_text_channel(name=f'random_{user.name}', category=self.random_category)
            await user.add_roles(self.member_role)
            try:
                await user.remove_roles(self.visitor_role)
            except:
                pass
            await ctx.response.send_message(f'Completely give {user.name} メンバー role', ephemeral=True)
        else:
            await ctx.response.send_message(f'{user.name} already has メンバー role', ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(
        memberize(bot)
    )