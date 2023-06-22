from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from playlist.db import (
    UsersDB,
    ConfigDB,
    PlaylistsDB,
    TracksDB,
    PlaylistTracksDB,
)

usersDB = UsersDB()
configDB = ConfigDB()
playlistsDB = PlaylistsDB()
tracksDB = TracksDB()
playlistTracksDB = PlaylistTracksDB()


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
    # check user config
    config = configDB.show_config(user.id)
    if config == 'create_playlist':
        # add playlist
        playlistsDB.add(user_id=user.id, name=update.message.text.strip().title())
        # set config
        configDB.set_config(user_id=user.id, status='start')
        # send message
        update.message.reply_html(
            f"Playlist created successfully!",
        )
    else:
        update.message.reply_html('siz  boshqa stage dasiz')


def show_playlists(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # get playlist
    playlists = playlistsDB.get_playlists(user.id)
    # send playlists
    inline_keyboards = []
    for playlist in playlists:
        inline_keyboards.append([InlineKeyboardButton(
            playlist['name'], 
            callback_data=f'playlist:{playlist["name"]}')]
        )
    update.message.reply_html(
        'Your playlists:',
        reply_markup=InlineKeyboardMarkup(inline_keyboards)
    )
    

def add_track(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # get playlist
    playlists = playlistsDB.get_playlists(user.id)
    # get track file id
    track_file_id = update.message.audio.file_id
    # add track to db
    track = tracksDB.add(user_id=user.id, file_id=track_file_id)
    # send playlists
    inline_keyboards = []
    for playlist in playlists:
        inline_keyboards.append([InlineKeyboardButton(
            playlist['name'], 
            callback_data=f'addT:{playlist["name"]}-{track}')]
        )
    # forward to message
    update.message.reply_html(
        'Select a playlist to add a track:',
        reply_markup=InlineKeyboardMarkup(inline_keyboards),
        reply_to_message_id=update.message.message_id
    )


def insert_track(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # get playlist name and track id
    playlist_name, track_id = update.callback_query.data.split(':')[1].split('-')
    # get track
    track = tracksDB.get_track(track_id)
    # insert track
    playlistTracksDB.add(playlist_name, track_id)
    # delete message
    update.callback_query.message.delete()
    # send message
    update.callback_query.message.reply_html(
        f"Track added to playlist <b>{playlist_name}</b>!",
    )


def show_tracks(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # get playlist name
    playlist_name = update.callback_query.data.split(':')[1]
    # get tracks
    tracks = playlistTracksDB.get_playlist_tracks(playlist_name)
    # send tracks
    for track in tracks:
        song = tracksDB.get_track(track['track_id'])
        update.callback_query.message.reply_audio(
            audio=song['file_id']
        )