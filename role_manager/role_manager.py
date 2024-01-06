import discord
import os
import sys
from discord import app_commands
from os.path import join, dirname
from dotenv import load_dotenv

#クライアントのセットアップ
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#tokenやidの取得
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
token = os.environ.get("TOKEN")                         #DiscordAPIのToken
guild_id = int(os.environ.get("GUILD_ID"))              #DiscordサーバーのID
member_role_id = int(os.environ.get("MEMBER_ID"))       #「メンバー」ロールのID
visitor_role_id = int(os.environ.get("VISITOR_ID"))     #「ビジター」ロールのID
random_category_id = int(os.environ.get("CATEGORY_ID")) #「雑談」カテゴリのID

@client.event
async def on_ready():
    global guild
    global member_role
    global visitor_role
    global random_category

    #オブジェクトの取得
    guild = client.get_guild(guild_id)
    member_role = guild.get_role(member_role_id)
    visitor_role=guild.get_role(visitor_role_id)
    random_category = guild.get_channel(random_category_id)
    await tree.sync(guild=guild)
    print("get on ready!")
    sys.stdout.flush()

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
async def memberize(ctx: discord.Interaction, user: discord.Member):
    if not(member_role in user.roles):  #ユーザがメンバーロールをもっていない場合のみ発火
        await guild.create_text_channel(name=f'random_{user}', category=random_category)
        await user.add_roles(member_role)
        try:
            await user.remove_roles(visitor_role)
        except:
            pass
        await ctx.response.send_message(f'Completely give {user} メンバー role', ephemeral=True)
    else:
        await ctx.response.send_message(f'{user} already has メンバー role', ephemeral=True)

client.run(token)