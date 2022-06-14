#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from datetime import datetime
from gzip import WRITE
import time
from cadastraBot import cancel
import models
import logging

from token_telegram import Token
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

WRITE, RESPOSTA = range(2)



def saudacao():

	mensagem = ""

	# obtém a hora atual para bom dia, boa tarde ou boa noite
	hora_atual = datetime.now().hour 
    
	if hora_atual < 12:
		mensagem = 'Olá!Bom dia!'
	elif 12 <= hora_atual < 18:
		mensagem = 'Olá!Boa tarde!'
	else:
		mensagem = 'Olá!Boa noite!'

	return  f"{mensagem}Eu sou o Tera, assistente virtual para comerçamos , digite o comentário de algum FILME "
    
def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
 
    mensagem = saudacao()
    update.message.reply_text(
        mensagem
    )
   
   
    return WRITE


def write_msg(update: Update, context: CallbackContext) -> int:
    
    msg = update.message.text
    modelo,vetor = models.get_modelo_vecto()
     
    resposta = models.get_sentindo(modelo,vetor , msg)
    update.message.reply_text(
        fr'Seu comentário é {resposta}. /cancel ou /start'
        
    )
    
    return RESPOSTA
    
def cancel(update: Update, context: CallbackContext) -> int:
    """Cancela a conversa com o usuário."""
    
    update.message.reply_text(
        'Até breve.'
    )
   
    return ConversationHandler.END   

def prox(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
 
    mensagem = 'Digite o comentário'
    update.message.reply_text(
        mensagem
    )
   
   
    return WRITE

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    tk = Token()
    tokentele = tk.get_token()
    updater = Updater(tokentele)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WRITE: [MessageHandler(Filters.text & ~Filters.command, write_msg)],
            RESPOSTA:[CommandHandler('start',prox)]
            },
            fallbacks=[MessageHandler(Filters.command, cancel)],
    )
   
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()