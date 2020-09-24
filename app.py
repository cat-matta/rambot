
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
# from telebot.credentials import bot_token, bot_user_name,URL
import requests
import re
import googleapi
import logging
import random
import secrets

TOKEN= ""
file=open("token.txt","r")
TOKEN=file.read()
#BOT_USERNAME= "@give_me_food"
file.close()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

text=["Что","You know what? Im just going to fucking kill myself. Thats what I'm going to fucking do. I am going to fucking blow my fucking brains out. I'm going to kill myself. I'm going to kill myself and it's going to be your fucking fault. You're a piece of shit, Diar. You're a fucking piece of garbage.","Diar you really got me this time, you win brother. You literally want to trigger my anxiety and depression and you are going to make me have a panic attack in front of my computer. You really are a selfish asshole that doesn't care about anyone but yourself. Stop trying to bait me into killing myself. You just want to see me die at this point by any means necessary. fuck you Diar you are not going to make me kill myself."]
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
	"""Send a message when the command /start is issued."""
	update.message.reply_text("Feeling like an indecisive couch potato? Worry not and use Botato to help you make a decision! Write /help for more info.\n")
	update.message.reply_text("Commands: \n/help --> how to use food bot.\n/diar --> roasts diar.\n/chuck -->returns Chuck Norris joke.\n/dog --> sends a random dog pic or gif.\n/meme --> sends the dankest memes.\n/maymay or /meemee --> finest collection of boomer hoomer.\n/cat --> praise the almighty inventor and get rewarded for it!\nThank.")


def help(update, context):
	"""Send a message when the command /help is issued."""
	#update.message.reply_text('Enter in thise order separated by a space: Zip code or location. Resturant or food type. Number of choices')
	#update.message.reply_text('Example: Central park pizza 4')
	update.message.reply_text('For now, you can only put a location and get all the food options there. Later on, there will be option to specify the type of food and how many entries show on the screen.')
	update.message.reply_text('Enter the location as so /central park. For best results, enter a specific zip code or distinct location(CCNY). If putting a home address, enter where it is. Be very specific with streets, "5th ave brooklyn" or "5th ave new york" as there are multiple 5th aves')
	update.message.reply_text("Enjoy!")

def give_food(update,context):
	"""Echo the user message."""
	# user_input,food_choice,size=input("Location. Food. Number: ").split()
	# location=googleapi.get_location(user_input)
	# choice=googleapi.top_five(location,food_choice,int(size))
	#update.message.reply_text(update.message.text)
	place=update.message.text
	update.message.reply_text("\nHere are {size} {food_choice} places near: {user_input}".format(size=5,food_choice="food",user_input=place))
	location=googleapi.get_location(str(place))
	results=googleapi.top_five(location,"food",5)
	update.message.reply_text(results)

def cat(update,context):
	update.message.reply_text("Hell yeah")
	contents=requests.get('http://aws.random.cat/meow').json()
	url=contents["file"]
	update.message.reply_text(url)

def chuck(update,context):
	contents=requests.get('https://api.chucknorris.io/jokes/random').json()
	value=contents['value']
	update.message.reply_text(value)

def dog(update,context):
	contents = requests.get('https://random.dog/woof.json').json()    
	url = contents["url"]
	update.message.reply_text(url)

def meme(update,context):
	contents=requests.get('https://meme-api.herokuapp.com/gimme/').json()
	url=contents['url']
	update.message.reply_text(url)
def maymay(update,context):
	contents=requests.get('https://meme-api.herokuapp.com/gimme/boomershumor').json()
	url=contents['url']
	update.message.reply_text(url)

def diar(update,context):
	num=secrets.randbelow(3)
	update.message.reply_text("@DiarSanakov")
	update.message.reply_text(text[num])
def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater(TOKEN, use_context=True)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("cat", cat))
	dp.add_handler(CommandHandler("diar", diar))
	dp.add_handler(CommandHandler("dog", dog))
	dp.add_handler(CommandHandler("meme", meme))
	dp.add_handler(CommandHandler("memes", meme))

	dp.add_handler(CommandHandler("maymay", maymay))
	dp.add_handler(CommandHandler("meemee", maymay))
	dp.add_handler(CommandHandler("maymays", maymay))
	dp.add_handler(CommandHandler("meemees", maymay))

	dp.add_handler(CommandHandler("chuck",chuck))
	dp.add_handler(MessageHandler(Filters.text | Filters.dice, give_food))
	#dp.add_handler(CommandHandler("givefood",give_food))

	# on noncommand i.e message - echo the message on Telegram
	
	# dp.add_handler(MessageHandler(Filters.text, give_food))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()