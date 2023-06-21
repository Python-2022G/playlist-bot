from telegram.ext import Updater, CommandHandler
import os
from playlist.callbacks import (
    start,
)

TOKEN = os.environ['TOKEN']

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
