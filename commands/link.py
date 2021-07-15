import config.config as config
import commands.admin as admin


async def main(message, prefix, client):
	if message.content.startswith(f"{prefix}link"):
		content = message.content.split(" ")
		
		if len(content) > 1 and content[1] == "set":
			if admin.perms(message.guild.id,message.author):
				text = ' '.join(content[2:])
				config.write(message.guild.id, "link", text)
			else:
				await admin.noperm(message)
		else:
			link = config.read(message.guild.id, "link")
			await message.channel.send(f"""{link}\n\nBot developed by <https://jcwyt.com>!""")