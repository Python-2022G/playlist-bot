from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import os
from playlist.callbacks import (
    start,
    choose_playlist_name,
    add_playlist,
    show_playlists,
    add_track,
    insert_track,
    show_tracks,
)

TOKEN = os.environ['TOKEN']

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text('🎵 Add Playlist'), choose_playlist_name))
    dp.add_handler(MessageHandler(Filters.text('📃 My Playlists'), show_playlists))
    dp.add_handler(MessageHandler(Filters.text, add_playlist))
    dp.add_handler(MessageHandler(Filters.audio, add_track))
    dp.add_handler(CallbackQueryHandler(insert_track, pattern='addT:'))
    dp.add_handler(CallbackQueryHandler(show_tracks, pattern='playlist:'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
