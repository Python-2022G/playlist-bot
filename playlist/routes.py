from playlist import app
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
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
bot = Bot(token=TOKEN)


@app.route('/wehbook', methods=['POST'])
def main():
    dp = Dispatcher(bot, None, workers=0)

    update = Update.de_json(request.get_json(force=True), bot)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text('🎵 Add Playlist'), choose_playlist_name))
    dp.add_handler(MessageHandler(Filters.text('📃 My Playlists'), show_playlists))
    dp.add_handler(MessageHandler(Filters.text, add_playlist))
    dp.add_handler(MessageHandler(Filters.audio, add_track))
    dp.add_handler(CallbackQueryHandler(insert_track, pattern='addT:'))
    dp.add_handler(CallbackQueryHandler(show_tracks, pattern='playlist:'))

    dp.process_update(update)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('https://codeschoolapp.pythonanywhere.com/wehbook')
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

