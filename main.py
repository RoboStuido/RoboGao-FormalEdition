#-----Discord module initial-----#
import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(case_insensitive=True, intents=intents)

#-----Import setting.json-----#
import json
with open('settings.json', 'r', encoding='utf8') as SETTINGS_JSON:
  settings = json.load(SETTINGS_JSON)

#-----Import cogs-----#
initial_extensions = []

import os
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    initial_extensions.append('cogs.' + filename[:-3])

if __name__ == '__main__':
  for extension in initial_extensions:
    bot.load_extension(extension)
    
#-----Other module-----#
from datetime import datetime

#-----Main module-----#
@bot.event
async def on_ready():
  #if not CurrentTime.is_running():
  #  bot.remove_application_command
  #  CurrentTime.start()
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='/help'))
  #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Datetime'))
  print('System: I\'m ready')

@tasks.loop(seconds=1)
async def CurrentTime():

  now = datetime.now()
  date_time = now.strftime("%Y-%m-%d %H:%M:%S")

  if int(now.strftime('%S'))%5 == 0:
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=date_time))

bot.run(settings['TOKEN'])