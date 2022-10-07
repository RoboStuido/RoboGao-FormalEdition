import discord
from discord import Option
from discord.ext import commands

import sys
import json
sys.path.append('..')
with open('settings.json', 'r', encoding='utf8') as SETTINGS_JSON:
  settings = json.load(SETTINGS_JSON)

class Tools(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.owner_id = settings['OWNER_ID']
  
  slash_command_guilds = settings['slash_command_guilds']

  @discord.slash_command(guild_ids=slash_command_guilds, name='ping', description='檢查延遲')
  async def ping(self, ctx: discord.ApplicationContext):
    await ctx.respond(f'延遲：{round(self.bot.latency*1000)} 毫秒', delete_after=5)

  @discord.slash_command(guild_ids=slash_command_guilds, name='getip', description='取得對外IP')
  async def getip(self, ctx: discord.ApplicationContext):
    if ctx.author.id == 331214580179271691:
      from requests import get
      ip = get('https://api.ipify.org').text
      await ctx.author.send(f'當前的對外IP是: {ip}')
      await ctx.respond(f'已傳送', delete_after=3)

    else :
      await ctx.respond(f'你沒有權限執行該指令', delete_after=3)

  @discord.slash_command(guild_ids=slash_command_guilds, name='ip', description='取得對外IP資訊')
  async def ip(self, ctx: discord.ApplicationContext):
    await ctx.respond(f'伺服器公開IP為: mps.us.to', delete_after=3)

  @discord.slash_command(guild_ids=slash_command_guilds, name='clear', description='清除未被釘選的訊息')
  async def clear(self, ctx: discord.ApplicationContext, amount: Option(int, '要清除的訊息數量',min=1, max=100, default=10)):
    if ctx.author.guild_permissions.manage_messages:
      deleted = await ctx.channel.purge(limit=amount, check=lambda msg: not msg.pinned)
      await ctx.respond(f'已刪除 {len(deleted)} 條訊息', delete_after=5)
    else :
      await ctx.respond(f'你沒有權限執行該指令!', delete_after=5)

  @discord.slash_command(guild_ids=slash_command_guilds, name='anyacursor', description='取得安妮亞游標的下載網址')
  async def sendmessage(self, ctx: discord.ApplicationContext):
    await ctx.respond(f'下載網址: https://cutt.ly/AnyaCursors')

def setup(bot):
  bot.add_cog(Tools(bot))