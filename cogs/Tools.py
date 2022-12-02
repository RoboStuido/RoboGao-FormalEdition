import discord
from discord import Option
from discord.ext import commands

from time import sleep

import sys
import json
sys.path.append('..')
with open('settings.json', 'r', encoding='utf8') as SETTINGS_JSON:
  settings = json.load(SETTINGS_JSON)

class Tools(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.owner_id = settings['OWNER_ID']
    self.TempChannel_json = './assets/TempChannel.json'
  
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
  async def anyacursor(self, ctx: discord.ApplicationContext):
    await ctx.respond(f'下載網址: https://cutt.ly/AnyaCursors')

  @discord.slash_command(guild_ids=slash_command_guilds, name='sourcecode', description='取得本機器人的源代碼')
  async def sendmessage(self, ctx: discord.ApplicationContext):
    await ctx.respond(f'源代碼在這: https://github.com/RoboStuido/RoboGao-FormalEdition')

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    if member.bot:
      sleep(500/1000)

    with open(self.TempChannel_json, 'a+') as f:
      with open(self.TempChannel_json, 'r+') as f:
        chs = json.load(f)

    if after.channel is not None:
      if str(after.channel) == "點我建立語音頻道":
        channel = await after.channel.clone(name=f'{member.name} 的語音')

        if channel is not None:
          await member.move_to(channel)
          
          if (f'{channel.guild.id}') in chs:
            chs[f'{channel.guild.id}'][f'{channel.id}'] = f'{channel}'
          else:
            chs[f'{channel.guild.id}'] = {}
            chs[f'{channel.guild.id}'][f'{channel.id}'] = f'{channel}'

          open(self.TempChannel_json, 'w').write(
            json.dumps(chs, sort_keys=True, indent=4, separators=(',', ': '))
          )

    if before.channel is not None:
      if str(before.channel) != "點我建立語音頻道":
        if (len(before.channel.members) == 0):
          try:
            if str(chs[f'{before.channel.guild.id}'][f'{before.channel.id}']) == str(before.channel):
              await before.channel.delete()
              del chs[f'{before.channel.guild.id}'][f'{before.channel.id}']
          except:
            pass

          try:
              if len(chs[f'{before.channel.guild.id}']) == 0:
                del chs[f'{before.channel.guild.id}']
          except:
            pass
      
          open(self.TempChannel_json, 'w').write(
            json.dumps(chs, sort_keys=True, indent=4, separators=(',', ': '))
          )

def setup(bot):
  bot.add_cog(Tools(bot))