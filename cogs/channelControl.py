import discord
from discord import Option
from discord.ext import commands

from time import sleep
from datetime import datetime

import sys
import json
sys.path.append('..')
with open('settings.json', 'r', encoding='utf8') as SETTINGS_JSON:
  settings = json.load(SETTINGS_JSON)

class channelControl(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.TempChannel_json = './assets/TempChannel.json'
  
  slash_command_guilds = settings['slash_command_guilds']

  @discord.slash_command(guild_ids=slash_command_guilds, name='wip_voicechanneluptime', description='獲取語音頻道存在時長')
  async def wip_voicechanneluptime(self, ctx: discord.ApplicationContext):
    try:
      channel = ctx.author.voice.channel
    except:
      await ctx.respond("請先加入語音頻道", ephemeral=True, delete_after=3)
      return

    with open(self.TempChannel_json, 'r+') as f:
      chs = json.load(f)

    createTime = datetime.strptime(chs[f'{channel.guild.id}'][f'{channel.id}'][f'create_at'], '%Y-%m-%d %H:%M:%S')

    _nowTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nowTime = datetime.strptime(_nowTime, '%Y-%m-%d %H:%M:%S')

    uptime = nowTime - createTime

    await ctx.respond(f'{channel.mention} 已經建立了 {uptime}', ephemeral=True)

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    if member.bot:
      sleep(1)

    with open(self.TempChannel_json, 'r+') as f:
      chs = json.load(f)

    if after.channel is not None:
      if str(after.channel) == "點我建立語音頻道":
        channel = await after.channel.clone(name=f'{member.display_name} 的語音')

        if channel is not None:
          await member.move_to(channel)
          
          if (f'{channel.guild.id}') not in chs:
            chs[f'{channel.guild.id}'] = {}
          
          chs[f'{channel.guild.id}'][f'{channel.id}'] = {}

          if (f'create_at' and f'name') not in chs[f'{channel.guild.id}'][f'{channel.id}']:
            chs[f'{channel.guild.id}'][f'{channel.id}'][f'create_at'] = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            chs[f'{channel.guild.id}'][f'{channel.id}'][f'name'] = f'{channel}'

    if before.channel is not None:
      if str(before.channel) != "點我建立語音頻道":
        if (len(before.channel.members) == 0):
          channel = before.channel
          try:
            if str(chs[f'{channel.guild.id}'][f'{channel.id}'][f'name']) == str(channel):
              await channel.delete()
              del chs[f'{channel.guild.id}'][f'{channel.id}']

            if len(chs[f'{channel.guild.id}']) == 0:
              del chs[f'{channel.guild.id}']
          except:
            pass

    open(self.TempChannel_json, 'w').write(
      json.dumps(chs, sort_keys=True, indent=4, separators=(',', ': '))
    )

def setup(bot):
  bot.add_cog(channelControl(bot))