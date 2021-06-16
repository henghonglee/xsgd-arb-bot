#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

import logging
import subprocess
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


def get_iron_supply(update: Update, _: CallbackContext) -> None:
    subprocess.run(["scrapy", "runspider", "crawler/spiders/iron_token_report_supply.py"])
    return ConversationHandler.END

def get_titan_supply(update: Update, _: CallbackContext) -> None:
    subprocess.run(["scrapy", "runspider", "crawler/spiders/titan_token_report_supply.py"])
    return ConversationHandler.END

def cancel(update: Update, _: CallbackContext) -> int:
    return ConversationHandler.END

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("1857941381:AAHPfQwENHSdjxmSyEJt0wutj8PDLZwf81Y")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('titan', get_titan_supply), CommandHandler('iron', get_iron_supply)],
        states={},
        fallbacks=[CommandHandler('cancel', cancel)],
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
