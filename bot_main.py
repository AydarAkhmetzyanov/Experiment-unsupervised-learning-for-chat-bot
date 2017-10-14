from telegram.ext import Updater, CommandHandler

from nlu_core import utterance_to_result

def start(bot, update):
    update.message.reply_text('Hello!')

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

updater = Updater('451683881:AAGYToQcvgGme6f9jPZFbqLjQt9smUkYiVA')

updater.dispatcher.add_handler(CommandHandler('start', start))


def echo(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text=utterance_to_result(update.message.text))

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
updater.dispatcher.add_handler(echo_handler)


updater.start_polling()
updater.idle()