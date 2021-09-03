import lib.regexLib as meese
import config.config as config
from discord.ext import commands
import discord


class RemoveMeese(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.MEESE_DELETED_MESSAGE = "Message flagged by meese detection. If this is a bug, contact bugs@jcwyt.com or report it on the Discord."
    self.MEESE_DELETED_DM_MESSAGE = "Message flagged by meese detection. This is a DM however, so the message cannot be deleted. ||But know that you've commited a sin||"

  @commands.Cog.listener() # @bot.event for Cogs
  async def on_message(self, message):
    if isinstance(message.channel, discord.channel.DMChannel):
      await message.reply(self.MEESE_DELETED_DM_MESSAGE)
      return
    try:
      if message.author.id != self.bot.user.id and message.author.id != 798016639089901610: # botwinkle is that ID
        if config.read(message.guild.id, "nomees") == "true":
          if ":meese:" in message.content.lower():
            await message.reply(self.MEESE_DELETED_MESSAGE)
            await message.delete()
            await self.bot.get_channel(864644173835665458).send(
              message.author.name + ": " + message.content
            ) # report in meese deletes
          else:
            string = meese.replaceWords(config.fetch(message.guild.id, "whitelist"), message.content, "")
            if meese.containsMeese(string):
              await message.reply(self.MEESE_DELETED_MESSAGE)
              await message.delete()
              await self.bot.get_channel(864644173835665458).send(
                message.author.name + ": " + message.content
              )
    except (discord.errors.NotFound, discord.errors.HTTPException): pass

  @commands.Cog.listener()
  async def on_message_edit(self, before, message):
    if isinstance(message.channel, discord.channel.DMChannel):
      await message.reply(self.MEESE_DELETED_DM_MESSAGE)
      return
    try:
      if message.author.id != self.bot.user.id and message.author.id != 798016639089901610: # botwinkle is that ID
        if config.read(message.guild.id, "nomees") == "true":
          if ":meese:" in message.content.lower():
            await message.reply("Message flagged by meese detection. If this is a bug, contact bugs@jcwyt.com or report it on the Discord.")
            await message.delete()
            await self.bot.get_channel(864644173835665458).send(
              message.author.name + ": " + message.content
            ) # report in meese deletes
          else:
            string = meese.replaceWords(config.fetch(message.guild.id, "whitelist"), message.content, "")
            if meese.containsMeese(string):
              await message.reply("Message flagged by meese detection. If this is a bug, contact bugs@jcwyt.com or report it on the Discord.")
              await message.delete()
              await self.bot.get_channel(864644173835665458).send(
                message.author.name + ": " + message.content
              ) # report in meese deletes
    except (discord.errors.NotFound, discord.errors.HTTPException): pass

def setup(bot):
  bot.add_cog(RemoveMeese(bot))
