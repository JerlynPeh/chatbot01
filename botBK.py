import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '572209278:AAGDaLmTlzs7OlssY1IUWxP75gwIFEdgt-E'

""" 
codes from  https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/inlinekeyboard.py
""""

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


""" 
My first codes  below
""""





def main():
	# Create the Updater and pass it your bot's token.
	updater = Updater(token=TOKEN)
        dispatcher = updater.dispatcher
        print('bot created.')


	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CallbackQueryHandler(button))
	dispatcher.add_handler(CommandHandler('help', help))
	dispatcher.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()


if __name__ == '__main__':
	main()
