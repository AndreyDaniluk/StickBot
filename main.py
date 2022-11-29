import telebot
import json
import random

class mem:
	json = json.loads(open("mem.json","r", encoding="utf8").read())

	def save():
		open("mem.json","w", encoding="utf8").write(json.dumps(mem.json, indent=4, ensure_ascii=False))

bot = telebot.TeleBot(mem.json["bot_settings"]["telegram_token"])

send_stick = 0
get_stick = 0

def addifnotexists(message):
	if mem.json["setting_gen"].get(str(message.chat.id), None) == None:
		mem.json["setting_gen"][str(message.chat.id)] = mem.json["bot_settings"]["default_gen_count"]
		mem.save()
		bot.reply_to(message, mem.json["bot_settings"]["not_be_before"])

@bot.message_handler(commands=["start"])
def startcommand(message):
	bot.reply_to(message, mem.json["bot_settings"]["hello_message"])
	addifnotexists(message)

@bot.message_handler(commands=["info"])
def startcommand(message):
	bot.reply_to(message, mem.json["bot_settings"]["info"].replace("{count_stickers}", str(len(mem.json["stickers_ids"]))).replace("{get_stick}", str(get_stick)).replace("{send_stick}", str(send_stick)))
	addifnotexists(message)

@bot.message_handler(commands=["setgen"])
def setgencommand(message):
	if " " in message.text:
		try:
			int(message.text.split(maxsplit=1)[1])
		except:
			bot.reply_to(message, mem.json["bot_settings"]["error_count_setgen"])
		else:
			if int(message.text.split(maxsplit=1)[1]) < 101 and int(message.text.split(maxsplit=1)[1]) > -1:
				gen_count = int(message.text.split(maxsplit=1)[1])
				mem.json["setting_gen"][str(message.chat.id)] = gen_count
				mem.save()
				bot.reply_to(message, mem.json["bot_settings"]["sussesfully_setgen"])
			else:
				bot.reply_to(message, mem.json["bot_settings"]["error_count_setgen"])
	else:
		bot.reply_to(message, mem.json["bot_settings"]["error_count_setgen"])


@bot.message_handler(content_types=['text'])
def textmessage(message):
	global send_stick
	addifnotexists(message)
	if mem.json["setting_gen"][str(message.chat.id)] > random.randint(0, 100):
		send_stick += 1
		bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(mem.json["stickers_ids"]))

@bot.message_handler(content_types=['sticker'])
def stickermessage(message):
	global get_stick
	global send_stick
	addifnotexists(message)
	get_stick += 1
	if not message.sticker.file_id in mem.json["stickers_ids"]:
		mem.json["stickers_ids"].append(message.sticker.file_id)
		mem.save()
	if mem.json["setting_gen"][str(message.chat.id)] > random.randint(0, 100):
		send_stick += 1
		bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(mem.json["stickers_ids"]))

print("Initialization successful, starting bot...")
bot.infinity_polling()