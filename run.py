from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from playlist.callbacks import (
    start,
    choose_playlist_name,
    add_playlist,
    show_playlists,
)

TOKEN = os.environ['TOKEN']

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text('🎵 Add Playlist'), choose_playlist_name))
    dp.add_handler(MessageHandler(Filters.text('📃 My Playlists'), show_playlists))
    dp.add_handler(MessageHandler(Filters.text, add_playlist))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
