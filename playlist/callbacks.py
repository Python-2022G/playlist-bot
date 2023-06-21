from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from playlist.db import (
    UsersDB,
    ConfigDB,
    PlaylistsDB,
)

usersDB = UsersDB()
configDB = ConfigDB()
playlistsDB = PlaylistsDB()


def start(update: Update, context: CallbackContext) -> None:
    # get user from update
    user = update.effective_user
    # insert user in db
    is_add = usersDB.add(
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username
    )
    # set config
    configDB.set_config(user_id=user.id, status='start')
    # keyboards
    keyboards = [
        [KeyboardButton('🎵 Add Playlist'), KeyboardButton('📃 My Playlists')],
    ]
    # send message
    if is_add:
        update.message.reply_html(
            f"Hello {user.mention_html()}! \n\nWelcome to <b>Playlist Bot</b>!",
            reply_markup=ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
        )
    else:
        update.message.reply_html(
            f"Hi {user.mention_html()}! \n\nWelcome back to <b>Playlist Bot</b>!",
            reply_markup=ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
        )


def choose_playlist_name(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # set config
    configDB.set_config(user_id=user.id, status='create_playlist')
    # send message
    update.message.reply_html(
        f"Select a name for your playlist",
    )


def add_playlist(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # add playlist
    playlistsDB.add(user_id=user.id, name=update.message.text.strip().title())
    # set config
    configDB.set_config(user_id=user.id, status='start')
    # send message
    update.message.reply_html(
        f"Playlist created successfully!",
    )
