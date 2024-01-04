import discord
from discord import app_commands
import os
from os.path import join, dirname
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#tokenやidの取得
token = os.environ.get("TOKEN")
guild_id = os.environ.get("GUILD_ID")
member_role_id = os.environ.get("MEMBER_ID")
visitor_role_id = os.environ.get("VISITOR_ID")
random_category_id = os.environ.get("CATEGORY_ID")


@client.event
async def on_ready():
    guild = client.get_guild(guild_id)
    await tree.sync(guild=guild)
    print("get on ready!")

#ユーザが加入した際にビジターロールを付与する
@client.event
async def on_member_join(member:discord.Member):
    guild = client.get_guild(guild_id)
    visitor_role = guild.get_role(visitor_role_id)
    await member.add_roles(visitor_role)

#指定されたユーザに個人randomチャンネルを作成し、メンバーロールを与える
@tree.command(
    name="memberize",
    description="指定されたユーザに個人用randomチャンネルを作成してメンバーロールを与えます。"
)
@discord.app_commands.guilds(guild_id)
async def vote(ctx: discord.Interaction, user: discord.Member):
    #オブジェクトの取得
    guild = client.get_guild(guild_id)
    member_role = guild.get_role(member_role_id)
    visitor_role=guild.get_role(visitor_role_id)
    random_category = guild.get_channel(random_category_id)

    await guild.create_text_channel(name=f'random_{user}', category=random_category)
    await user.add_roles(member_role)
    await user.remove_roles(visitor_role)
    await ctx.response.send_message("ok", ephemeral=True)

client.run(token)