from telegram import Update
from telegram.ext import CallbackContext
from playlist.db import (
    UsersDB,
    ConfigDB,
)

usersDB = UsersDB()
configDB = ConfigDB()


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
    # send message
    if is_add:
        update.message.reply_html(
            f"Hello {user.mention_html()}! \n\nWelcome to <b>Playlist Bot</b>!"
        )
    else:
        update.message.reply_html(
            f"Hi {user.mention_html()}! \n\nWelcome back to <b>Playlist Bot</b>!"
        )
