import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import random


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '572209278:AAGDaLmTlzs7OlssY1IUWxP75gwIFEdgt-E'

STEP = 0
CHOICE = [0, 0]
tempNum = 0

""" 
codes from  https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/inlinekeyboard.py
"""
'''
def start(bot, update):
	keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

	reply_markup = InlineKeyboardMarkup(keyboard)

	update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(bot, update):
	query = update.callback_query

	bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def help(bot, update):
	update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)
'''


""" 
My first codes  below
"""
	


def start(bot, update):
	print 'start()'
	global STEP

	STEP = 1
	keyboard = [[InlineKeyboardButton("Stall", callback_data='001'),
                 InlineKeyboardButton("Food", callback_data='010')],

                [InlineKeyboardButton("Both", callback_data='011'),InlineKeyboardButton("None", callback_data='000')],
[InlineKeyboardButton("Its okay. Thanks!", callback_data='x')]
]

	reply_markup = InlineKeyboardMarkup(keyboard)

	update.message.reply_text('Hi there! Seems like you need a hand deciding what to eat today. \n Which have you decided so far?', reply_markup=reply_markup)

def button(bot, update):
	print 'button()'
	global CHOICE
	query = update.callback_query
	uchoice = query.data
	#if choice == 'x': end

	if uchoice == '001':
		CHOICE[0] = 1

		bot.edit_message_text(text='How many FOOD DISHES are you deciding between? (Enter a digit/number)',chat_id=query.message.chat_id,message_id=query.message.message_id)	
		
	elif uchoice == '010':
		CHOICE[1] = 2
		
		bot.edit_message_text(text='How many STALLS are you choosing from? (Enter a digit/number)',chat_id=query.message.chat_id,message_id=query.message.message_id)

	elif uchoice == '011':
		CHOICE = [1, 2]
		bot.edit_message_text(text='logic1 for this is coming soon! Wait for it.',chat_id=query.message.chat_id,message_id=query.message.message_id)

	else:
		bot.edit_message_text(text='logic2 for this is coming soon! Wait for it.',chat_id=query.message.chat_id,message_id=query.message.message_id)
		

	
	#bot.edit_message_text(text="Selected option: {}".format(query.data),chat_id=query.message.chat_id,message_id=query.message.message_id)	


def get_user_reply(bot, update):
	print 'get_user_reply()'
	# validate Y/N input

	global STEP, tempNum, CHOICE

	#TODO: validate to ensure int and not crazy number and not empty 


	inputVal = int(update.message.text)
	print 'update.message.text, len:'
	print update.message.text
	print len(update.message.text)
	
	choice_count = CHOICE[0] + CHOICE[1]
	
	if STEP == 1 and inputVal > 1:	
		tempNum = inputVal
		STEP = 2
	else:
		print 'tomato: validate user input'
		
	if STEP == 2:
		

		if choice_count == 1:
			update.message.reply_text('Next, assign each food/dish a number between 1 to ' + repr(tempNum) + '. \nEnter /gen when you have done so.')
			print 'banana'
		
		elif choice_count == 2:
			update.message.reply_text('Next, assign a number to each Stall between 1 to ' + repr(tempNum) + '. \nEnter /gen when your done!')
			print 'papaya'
		else:
			print 'logic coming soon.'
		STEP = 3

def generate_random(bot, update):
	print 'generate_random()'
	update.message.reply_text('~Bzzt Bzzt~')
	update.message.reply_text('How about '+ repr(random.randint(1,tempNum)) + '?')
	
		
 	
def cancel(bot, update):
	user = update.message.from_user
	update.message.reply_text('Thank you! Hope you\'ve decided on what to eat. Talk to you soon!')	

def help(bot, update):
	update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)	

## main 
def main():
	# Create the Updater and pass it your bot's token.
	updater = Updater(token=TOKEN)
        dispatcher = updater.dispatcher
        print('bot created.')

	getUserReply_handler = MessageHandler(Filters.text, get_user_reply)
	

	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CallbackQueryHandler(button))
	dispatcher.add_handler(CommandHandler('gen', generate_random))
	
	dispatcher.add_handler(getUserReply_handler)
	dispatcher.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()


if __name__ == '__main__':
	main()
