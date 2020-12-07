
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
# from telebot.credentials import bot_token, bot_user_name,URL
from flask import Flask
import requests
import re
import googleapi
import logging
import random
import secrets
import os
from dotenv import load_dotenv
load_dotenv()

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ.get("token")
# file=open("token.txt","r")
# TOKEN = file.read()

# file.close()
app = Flask(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
	"""Send a message when the command /start is issued."""
	update.message.reply_text("Feeling like an indecisive couch potato? Worry not and use Botato to help you make a decision! Write /help for more info.\n")
	update.message.reply_text("Commands: \n/help --> how to use food bot.\n/chuck --> returns Chuck Norris joke.\n/dog --> sends a random dog pic or gif.\n/meme --> sends the dankest memes.\n/maymay or /meemee --> finest collection of boomer hoomer.\n/cat --> praise the almighty inventor and get rewarded for it!\nThank.")


def help(update, context):
	"""Send a message when the command /help is issued."""
	update.message.reply_text("UPDATE: Feature currently broken.")
	update.message.reply_text('Enter in thise order separated by a comma and space: Zip code or location. Resturant or food type. Number of choices.\nIf you dont want to specify a food type just put a blank space there or a 0 and it will default to just food places.\n')
	update.message.reply_text('Example1: /food Central park, thai, 4 --> would give 4 nearest thai places by Central park\nExample2: /food CCNY --> would give 5 general food places by CCNY\nExample3: /food CCNY, pizza --> would give 5 pizza places by CCNY\nExample4: /food CCNY, 0, 10 --> would give the nearest 10 food places by CCNY\nExample5: /food CCNY, , 10 --> would give the nearest 10 food places by CCNY')
	update.message.reply_text("Enjoy!")

def give_food(update,context):
	place = context.args
	place, food_choice, number = (" ".join(place).split(", ")+[None]+[None])[:3] # for user to specify choices, does not account for if the user wants to put in a food
	if(food_choice is None or food_choice == "" or food_choice == "0" or number is None): #temporary fix for default values
		if(food_choice is None or food_choice == "" or food_choice == "0"):
			food_choice = 'food'
		if(number is None):
			number = 5

	update.message.reply_text("\nHere are {size} {food_choice} places near: {user_input}".format(size=number,food_choice=food_choice,user_input=place))
	# location = googleapi.get_location(str(place))
	# results = googleapi.top_five(location,food_choice,int(number))
	# update.message.reply_text(results)
	update.message.reply_text("Feature unavailable, must enable Google billing :(")
	
def cat(update,context):
	update.message.reply_text("Hell yeah")
	contents = requests.get('http://aws.random.cat/meow').json()
	url = contents["file"]
	update.message.reply_text(url)

def chuck(update,context): #chuck norris jokes haha
	contents = requests.get('https://api.chucknorris.io/jokes/random').json()
	value = contents['value']
	update.message.reply_text(value)

def dog(update,context): 
	contents = requests.get('https://random.dog/woof.json').json()    
	url = contents["url"]
	update.message.reply_text(url)

def meme(update,context):
	contents = requests.get('https://meme-api.herokuapp.com/gimme/').json()
	url = contents['url']
	update.message.reply_text(url)

def maymay(update,context): #boomermeems
	contents = requests.get('https://meme-api.herokuapp.com/gimme/boomershumor').json()
	url = contents['url']
	update.message.reply_text(url)



def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)

@app.route('/')
def main():
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater(TOKEN, use_context=True)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	
	#the main stuff
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("food",give_food))

	#is it memes
	dp.add_handler(CommandHandler("meme", meme))
	dp.add_handler(CommandHandler("memes", meme))

	#or maymays?
	dp.add_handler(CommandHandler("maymay", maymay))
	dp.add_handler(CommandHandler("meemee", maymay))
	dp.add_handler(CommandHandler("maymays", maymay))
	dp.add_handler(CommandHandler("meemees", maymay))

	#limited edition
	dp.add_handler(CommandHandler("cat", cat))
	dp.add_handler(CommandHandler("dog", dog))
	dp.add_handler(CommandHandler("chuck",chuck))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()
	#updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
	#updater.bot.setWebhook('https://rambotato.herokuapp.com/' + TOKEN)
	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
	#port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0')