from hashlib import new
import discord
from discord.ext import commands
import json

from discord import File
from typing import Optional
from easy_pil import Canvas, Editor, Font, Text, load_image_async

import string
import random
import time
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

import sys
sys.path.append('..')
with open('settings.json', 'r', encoding='utf8') as SETTINGS_JSON:
  settings = json.load(SETTINGS_JSON)
slash_command_guilds = settings['slash_command_guilds']

def generate_random_password(password_length):
	## length of password from the user
	length = password_length

	## shuffling the characters
	random.shuffle(characters)
	
	## picking random characters from the list
	password = []
	for i in range(length):
		password.append(random.choice(characters))

	## shuffling the resultant password
	random.shuffle(password)

	## converting the list to string
	## printing the list
	return ("".join(password))

async def CreateBanner(self, userr, percent, xp, next_level_xp, level):
    ##Rank Card
    background = Editor(Canvas((934, 282), "#23272a"))
    profile = await load_image_async(str(userr.display_avatar))
    profile = Editor(profile).resize((190, 190)).circle_image()

    Name_Font = Font(path='./assets/LevelSystem/NotoSans_TC/NotoSansTC-Medium.otf', size=50)
    Xp_Font = Font(path='./assets/LevelSystem/NotoSans_TC/NotoSansTC-Medium.otf', size=40)
    Level_Font = Font.poppins(size=60)

    background.rectangle((20, 20), 894, 242, "#2a2e35")
    background.paste(profile, (50, 50))

    def StatusCircle(a):
      background.ellipse((42, 42), width=206, height=206, outline=a, stroke_width=10)

    if(str(userr.status) == 'online') :
      StatusCircle('#43b581')
    if (str(userr.status) == 'offline' or userr.status == 'invisible'):
      StatusCircle('#747f8d')
    if (str(userr.status) == 'idle'):
      StatusCircle('#faa81a')
    if (str(userr.status) == 'dnd'):
      StatusCircle('#ed4245')

    background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=10)
    background.bar(
        (260, 180),
        max_width=630,
        height=40,
        percentage=percent,
        fill="#00fa81",
        radius=10,
    )

    background.text((270, 120), str(userr.display_name), font=Name_Font, color="#00fa81")
    background.text(
      (870, 125),
      f'XP: {xp} / {next_level_xp}',
      font=Xp_Font,
      color="#00fa81",
      align="right",
    )

    background.text(
      (850, 50),
      f"LEVEL {level}",
      font=Level_Font,
      color='#1EAAFF',  
      align="right"
    )

    return File(fp=background.image_bytes, filename='./assets/LevelSystem/bg.png')

class levelSystem(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.json_path = './assets/LevelSystem/LevelsData.json'

  @commands.Cog.listener()
  async def on_message(self, message):
    if not message.content.startswith('?'):
      if not message.author.bot:
        with open(self.json_path, 'r') as f:
          data = json.load(f)

        data_format = (f'{int(message.guild.id)}-{str(message.author.id)}')

        if data_format in data:
          
          xp = data[data_format]['xp']
          level = data[data_format]['level']

          increased_xp = xp + 5
          new_level = int(increased_xp / 100)

          data[data_format]['xp'] = increased_xp

          with open(self.json_path, 'w') as f:
            json.dump(data, f, indent=4)

          if new_level > level:

            bot_info = await self.bot.application_info()
            owner = bot_info.owner

            await message.channel.send(f'恭喜 **{message.author.mention}** 升上 **{new_level}** 等！')

            data[data_format]['xp'] = 0
            data[data_format]['level'] = new_level

            with open(self.json_path, 'w') as f:
              json.dump(data, f, indent=4)

        else:
          data[data_format] = {}
          data[data_format]['xp'] = 5
          data[data_format]['level'] = 1
          
          with open(self.json_path, 'w') as f:
            json.dump(data, f, indent=4)

  @discord.slash_command(guild_ids=slash_command_guilds, name='rank', descrtiption='查看等級')
  async def rank(self, ctx: discord.ApplicationContext, user: Optional[discord.Member]):
    userr = user or ctx.author
    data_format = (f'{int(ctx.guild.id)}-{str(userr.id)}')

    with open(self.json_path, 'r') as f:
      data = json.load(f)

    if data_format in data:
    
        xp = data[data_format]["xp"]
        level = data[data_format]["level"]

        next_level_xp = int((level + 1) * 100)
        xp_need = next_level_xp
        xp_have = data[data_format]['xp']

        percentage = int(((xp_have*100) / xp_need))

        card = await CreateBanner(self, userr, percentage, xp, next_level_xp, level)
        await ctx.respond(file=card)

    else:
      data[data_format] = {}
      data[data_format]['xp'] = 0
      data[data_format]['level'] = 1
      
      with open(self.json_path, 'w') as f:
        json.dump(data, f, indent=4)

      xp = data[data_format]["xp"]
      level = data[data_format]["level"]
      next_level_xp = int((level + 1) * 100)
      xp_need = next_level_xp
      xp_have = data[data_format]['xp']
      percentage = int(((xp_have*100) / xp_need))

      card = await CreateBanner(self, userr, percentage, xp, next_level_xp, level)
      await ctx.respond(file=card)

  #@commands.command(name='leaderboard', aliases=['lb'])
  #async def leaderboard(self, ctx, range_num = 10):
  #  with open(self.json_path, 'r') as f:
  #    data = json.load(f)
#
  #  l = {}
  #  total_xp = []
#
  #  for user_id in data:
  #    xp = int(data[str(user_id)]['xp'] + (int(data[str(user_id)]['level']) * 100))
#
  #    l[xp] = f"{user_id}';{data[str(user_id)]['level']};{data[str(user_id)]['xp']}"
  #    total_xp.append(xp)
#
  #  total_xp = sorted(total_xp, reverse=True)
  #  index = 1
#
  #  mbed = discord.Embed(title='排行榜', color=0x00ff00)
#
  #  for amt in total_xp:
  #    id_ = int(str(l[amt]).split(';')[0])
  #    level = int(str(l[amt]).split(';')[1])
  #    xp = int(str(l[amt]).split(';')[2])
#
  #    #member = await ctx.guild.get_member(id_)
  #    member = await self.bot.fetch_user(id_)
#
  #    if member is not None:
  #      name = member.name
  #      mbed.add_field(
  #        name=f'{index}. {name}',
  #        value=f'**等級: {level}\n經驗值: {xp}**',
  #        inline=False
  #      )
#
  #      if index == range_num:
  #        break
  #      else:
  #        index += 1
#
  #  await ctx.send(embed=mbed)


def setup(client):
  client.add_cog(levelSystem(client))