from discord.ext import commands
import lib.admin as admin
import mediawiki
import aiohttp
import os
from typing import Optional

QA_URL = "https://api-inference.huggingface.co/models/bert-large-uncased-whole-word-masking-finetuned-squad"
GPT_NEO_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"

headers = {"Authorization": f"Bearer {os.getenv('API_TOKEN')}"}

async def query(payload, url=QA_URL, parameters={}, options={}):
  body = {"inputs":payload,'parameters':parameters,'options':options}
  async with aiohttp.ClientSession() as cs:
    async with cs.post(url, headers=headers, json=body) as response:
      answer = await response.json()
      return answer
#%prompt 4 I'm an engineer constructing cutting edge transportation
class HuggingfaceAI(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.wikipedia = mediawiki.MediaWiki()

  @commands.command(name='textgen', aliases=['prompt'])
  async def textGen(self, ctx, length: Optional[int]=-1, temperature: Optional[float]=0.5, *, prompt: str):
    answer = await ctx.send("Waiting for GPT-NEO")
    minimumTokenLength = 6
    if admin.perms(ctx):
      minimumTokenLength = 1
    if (length > 500 or length < minimumTokenLength) and length != -1:
      await ctx.send(f"Sorry, token length of {length} is invalid. Either it's too big, or too small. Please try a different length. My personal favorite is 40, which will output one or two sentences.")
      return
    try:
      reqJSON = {"repetition_penalty": 20.0, "temperature": temperature, "return_full_text": False}
      if length != -1:
        reqJSON += {"max_length": length}
      rawAnswer = await query(prompt, GPT_NEO_URL, )
      answerText = prompt + rawAnswer[0]['generated_text']
    except KeyError:
      await ctx.send(f"Sorry, an unexpected `KeyError` was encountered talking to the API. Please report bugs in the JCWYT Discord, or by contacting bugs@jcwyt.com. When you report the error, give us this: ```json\n{str(rawAnswer)}\n```")
      return
    await ctx.send(answerText)

  @commands.command(name='igotaquestion', aliases=['plzihavequestion', 'readthisandanswermyquestion', 'aiqa', 'ask'])
  async def aiqa(self, ctx, wikipediaPageTitle: str=None, *, quesion: str):
    answer = await ctx.send("Waiting for Wikipedia...")
    try:
      summary = self.wikipedia.page(wikipediaPageTitle).summarize(10)
    except mediawiki.exceptions.DisambiguationError as e:
      await answer.edit(f"Sorry, there's multiple Wikipedia articles going by similar names to what you requested I look at. Look at this list and see which one you want: {str(e)[:30] + (str(e)[30:] and '...')}")
      return
    except mediawiki.exceptions.PageError:
      await answer.edit("Sorry, no Wikipedia page by the requested title was found.")
      return
    except mediawiki.exceptions.HTTPTimeoutError:
      await answer.edit("Sorry, the Mediawiki servers timed out. Maybe try again later idk")
      return
    except mediawiki.exceptions.RedirectError:
      await answer.edit("Sorry, the Wikipedia page unexpectedly resolved to a redirect.")
      return
    await answer.edit("Waiting for bert-large-uncased-whole-word-masking-finetuned-squad...")
    answerText = (await query({
      "inputs": {
        "question": quesion,
        "context": summary,
      },
    }))['answer']
    await answer.edit(answerText)

def setup(bot):
  bot.add_cog(HuggingfaceAI(bot))