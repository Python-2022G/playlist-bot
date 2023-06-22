from tinydb import TinyDB, Query
from tinydb.table import Document


class UsersDB:
    def __init__(self):
        db = TinyDB('db/users.json', indent=4)
        self.users = db.table('users')
    
    def is_user(self, user_id):
        return self.users.contains(doc_id=user_id)

    def add(self, user_id, first_name, last_name=None, username=None):
        if not self.is_user(user_id):
            doc = Document(
                doc_id=user_id,
                value={
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username
                }
            )
            self.users.insert(doc)
            return True
        return False


class PlaylistsDB:
    def __init__(self):
        db = TinyDB('db/playlists.json', indent=4)
        self.playlists = db.table('playlists')

    def is_playlist(self, playlist_id, user_id):
        return self.playlists.contains(
            (Query().user_id == user_id) & (Query().doc_id == playlist_id)
        )

    def add(self, user_id, name):
        return self.playlists.insert({
            'user_id': user_id,
            'name': name
        })
    
    def get_playlists(self, user_id):
        return self.playlists.search(Query().user_id == user_id)

    def delete(self, playlist_id, user_id):
        self.playlists.remove(
            (Query().user_id == user_id) & (Query().doc_id == playlist_id)
        )


class TracksDB:
    def __init__(self):
        db = TinyDB('db/tracks.json', indent=4)
        self.tracks = db.table('tracks')

    def is_track(self, track_id):
        return self.tracks.contains(doc_id=track_id)

    def add(self, user_id, file_id):
        return self.tracks.insert({
            'user_id': user_id,
            'file_id': file_id
        })
    
    def get_track(self, track_id):
        if self.is_track(track_id):
            return self.tracks.get(doc_id=track_id)
        return None

    def delete(self, track_id):
        self.tracks.remove(doc_ids=[track_id])


class PlaylistTracksDB:
    def __init__(self):
        db = TinyDB('db/playlist_tracks.json', indent=4)
        self.playlist_tracks = db.table('playlist_tracks')

    def is_playlist_track(self, playlist_id, track_id):
        return self.playlist_tracks.contains(
            (Query().playlist_id == playlist_id) & (Query().track_id == track_id)
        )

    def add(self, playlist_id, track_id):
        return self.playlist_tracks.insert({
            'playlist_id': playlist_id,
            'track_id': track_id
        })

    def get_playlist_tracks(self, playlist_id):
        return self.playlist_tracks.search(Query().playlist_id == playlist_id)

    def delete(self, playlist_id, track_id):
        self.playlist_tracks.remove(
            (Query().playlist_id == playlist_id) & (Query().track_id == track_id)
        )


class ConfigDB:
    def __init__(self):
        db = TinyDB('db/config.json', indent=4)
        self.config = db.table('config')

    def set_config(self, user_id, status):
        if self.config.contains(doc_id=user_id):
            self.config.update({'status': status}, doc_ids=[user_id])
        else:
            doc = Document(
                doc_id=user_id,
                value={
                    'status': status
                }
            )
            self.config.insert(doc)
    
    def show_config(self, user_id):
        if self.config.contains(doc_id=user_id):
            return self.config.get(doc_id=user_id)['status']
        return None