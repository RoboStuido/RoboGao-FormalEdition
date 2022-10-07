from email.policy import default
from lib2to3.pgen2.token import OP
import string
import discord
from discord import Option
from discord.ext import commands

import sys
import json
sys.path.append('..')
with open('settings.json', 'r', encoding='utf8') as SETTINGS_JSON:
  settings = json.load(SETTINGS_JSON)

class Imgs(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  slash_command_guilds = settings['slash_command_guilds']

  @discord.slash_command(guild_ids=slash_command_guilds, name='otter', description='可愛的水獺GIF')
  async def otter(self, ctx: discord.ApplicationContext, member: Option(discord.Member, 'Tag?', default=False)):
    otterGIF = 'https://imgur.com/YmtXwmS'
    if member:
      await ctx.respond(f'{member.mention}')
      await ctx.channel.send(otterGIF)
    else:
      await ctx.respond(otterGIF)

  @discord.slash_command(guild_ids=slash_command_guilds, name='h_shiba', description='不可以色色')
  async def h_shiba(self, ctx: discord.ApplicationContext, member: Option(discord.Member, 'Tag?', default=False)):
    h_shiba = 'https://imgur.com/OB8svJ9'
    if member:
      await ctx.respond(f'{member.mention}')
      await ctx.channel.send(h_shiba)
    else:
      await ctx.respond(h_shiba)

  @discord.slash_command(guild_ids=slash_command_guilds, name='same_incense', description='鯊鯊幫你上香')
  async def same_incense(self, ctx: discord.ApplicationContext, member: Option(discord.Member, 'Tag?', default=False)):
    same_incense = 'https://imgur.com/zdJCgdY'
    if member:
      await ctx.respond(f'{member.mention}')
      await ctx.channel.send(same_incense)
    else:
      await ctx.respond(same_incense)

  @discord.slash_command(guild_ids=slash_command_guilds, name='same_incense_wbg', description='鯊鯊幫你上香(白背景)')
  async def same_incense_wbg(self, ctx: discord.ApplicationContext, member: Option(discord.Member, 'Tag?', default=False)):
    same_incense_wbg = 'https://imgur.com/fMrmmxk'
    if member:
      await ctx.respond(f'{member.mention}')
      await ctx.channel.send(same_incense_wbg)
    else:
      await ctx.respond(same_incense_wbg)

  @discord.slash_command(guild_ids=slash_command_guilds, name='capoo_dancing', description='咖波跳舞')
  async def capoo_dancing(self, ctx: discord.ApplicationContext, member: Option(discord.Member, 'Tag?', default=False)):
    capoo_dancing = 'https://imgur.com/Kd4bFH3'
    if member:
      await ctx.respond(f'{member.mention}')
      await ctx.channel.send(capoo_dancing)
    else:
      await ctx.respond(capoo_dancing)

def setup(bot):
  bot.add_cog(Imgs(bot))