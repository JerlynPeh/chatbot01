import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import random


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = 'YOUR TOKEN'



tempNum = 0

FLIST = []
SLIST = []

""" 
My first codes  below
"""
	


def start(bot, update):
	print 'start()'

	update.message.reply_text('Hi there! Seems like you need a hand deciding what to eat today. \n Tell me your choices in either of the following formats: \n 1. porridge, rice, yellow noodles  \n 2. stall 1, stall 2, stall 3 \n 3. Stall 1-porridge, Kfc-mashed potato, Seng Kee-herbal mee sua')


def process_user_reply(bot, update):
	print 'process_user_reply()'
	# validate Y/N input

	global FLIST, SLIST, tempNum

	#TODO: validate to ensure int and not crazy number and not empty 

	update.message.reply_text('Hold on~ Bot is thinking which you should choose~ Give bot awhile...')
	
	print update.message.text
	

	inputData =  update.message.text

	if len(inputData) == 0:
		update.message.reply_text('Oops, seems like theres nothing to choose from. Enter /start to start again!')
		

	#reinitialize the global variables for this session
	SLIST =[]
	FLIST = []
	tempNum = 0

	if (validate_input(inputData)):
		try:
			if '-' in inputData:
				SLpairs = inputData.split(',')
			
				for pair in SLpairs:
					SLIST.append(pair.split('-')[0].strip())
					FLIST.append(pair.split('-')[1].strip())
				#gotta ensure both lists have same length

				if len(SLIST) != len(FLIST): raise ValueError('list lengths dont match!')
				print 'SLIST len: ' + repr(len(SLIST))
				print 'FLIST len: ' + repr(len(FLIST))
			else:
				FLIST = inputData.split(',')
				print 'FLIST len: ' + repr(len(FLIST))

			if (len(SLIST) <= 1 and len(FLIST) <= 1) or len(FLIST) <= 1: 
				update.message.reply_text('Seems like you have decided. So Toodles!')
				cancel(bot, update)

			tempNum = len(FLIST)-1
			update.message.reply_text('Enter /gen to choose an option for you!')

		except Exception as e:
			update.message.reply_text('Oops! An error occured somewhere. Please use /start to try again. What a bummer :( ')
	else:
		update.message.reply_text('Enter your choices in the suggested format please!')		
		
			
	
def validate_input(inputStr):
	if (',' not in inputStr) or ('-' in inputStr and ',' not in inputStr) or len(inputStr)< 4: return False
	
	return True

		
def generate_random(bot, update):
	print 'generate_random()'
	update.message.reply_text('~Bzzt Bzzt~')
	

	opt = random.randint(0,tempNum)
	if len(SLIST) > 1:
		
		update.message.reply_text('Hmm.. How about '+ SLIST[opt].upper() + ' ' + FLIST[opt].upper() + '?')
	else:
		update.message.reply_text('Perhaps '+ FLIST[opt].upper() + '?')
	
		
 	
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

	procUserReply_handler = MessageHandler(Filters.text, process_user_reply)
	

	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CommandHandler('gen', generate_random))
	dispatcher.add_handler(CommandHandler('done', cancel))
	dispatcher.add_handler(CommandHandler('ok', cancel))
	
	dispatcher.add_handler(procUserReply_handler)
	dispatcher.add_error_handler(error)
	dispatcher.add_error_handler(cancel)

	# Start the Bot
	updater.start_polling()

	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()


if __name__ == '__main__':
	main()
