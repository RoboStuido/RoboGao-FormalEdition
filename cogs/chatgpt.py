from datetime import datetime
import discord
from discord.ext import commands

import sys
import json
sys.path.append('..')
with open('settings.json', 'r', encoding='utf8') as SETTINGS_JSON:
  settings = json.load(SETTINGS_JSON)

import openai
openai.api_key = settings["OpenAI_API_KEY"]

class ChatGPT(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.slash_command(name='chat', description='來自 OpenAI 的 ChatGPT')
  async def chat(self, ctx:discord.ApplicationContext, *, content: discord.Option(str, '內容', min_length=1), hide: discord.Option(bool, '私人訊息?', default=False)):
    await ctx.response.defer()

    completion = openai.Completion.create(
      engine = 'text-davinci-003',
      prompt = content,
      max_tokens = 1024,
      n = 1,
      temperature = 0.5,
    )
  
    result = completion.choices[0].text

    try:
      if hide:
        await ctx.followup.send(f'生成完畢!', delete_after=3)
        await ctx.author.send(f'{result}')
      else:
        await ctx.followup.send(f'{result}')
    except:
      timestamp = datetime.now()
      print(f"{timestamp}: Send failed!")
  
def setup(bot):
  bot.add_cog(ChatGPT(bot))