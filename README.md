# playlist-bot

This project is Telegram bot for creating playlists.

## Features

- Create playlists
- Add tracks to playlists
- Remove tracks from playlists
- Get playlists
- Get tracks from playlists

## Project structure

```
.
├── playlist
│   ├── __init__.py
│   ├── db.py
│   ├── callbacks.py
│   ├── routes.py
├── requirements.txt
├── db.json
├── README.md
├── .gitinore
├── run.py
```

## Database Structure

Tables:

- users
- playlists
- tracks
- playlist_tracks
- config

Users:

```json
{
    "users": {
        "id": {
            "username": "username",
            "first_name": "first_name",
            "last_name": "last_name"
        }
    }
}
```

Playlists:

```json
{
    "playlists": {
        "id": {
            "name": "name",
            "user_id": "user_id"
        }
    }
}
```

Tracks:

```json
{
    "tracks": {
        "id": {
            "file_id": "file_id"
        }
    }
}
```

Playlist Tracks:

```json
{
    "playlist_tracks": {
        "id": {
            "playlist_id": "playlist_id",
            "track_id": "track_id"
        }
    }
}
```

Config:

```json
{
    "config": {
        "chat_id": {
            "status": "create-playlist",
        }
    }
}
```
