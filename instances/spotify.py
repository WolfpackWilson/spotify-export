import os
import sqlite3

import spotipy

TABLE_EXISTS = os.path.isfile("spotify.db")
USER = 123
STARTING_OFFSET = 0
LIMIT = 20

con = sqlite3.connect("spotify.db")
cur = con.cursor()

sp = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-library-read"
    )
)

if not TABLE_EXISTS:
    with open('create_table.sql') as f:
        cur.executescript(f.read())
        con.commit()

offset = STARTING_OFFSET
playlist = sp.current_user_saved_tracks(limit=LIMIT, offset=offset)
print(f'{offset} songs completed')
while playlist['items']:
    for idx, item in enumerate(playlist['items']):
        track = item['track']
        cur.execute("INSERT OR IGNORE INTO Tracks VALUES (?,?,?,?,?,?,?,?,?,?)", (
            track['id'],
            track['album']['id'],
            track['disc_number'],
            track['duration_ms'],
            track['explicit'],
            track['external_ids'].get('isrc', None),
            track['name'],
            track['popularity'],
            track['preview_url'],
            track['uri']
        ))

        features = sp.audio_features(track['id'])[0]
        cur.execute("INSERT OR IGNORE INTO AudioFeatures VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            features['id'],
            features['acousticness'],
            features['danceability'],
            features['energy'],
            features['instrumentalness'],
            features['key'],
            features['liveness'],
            features['loudness'],
            features['mode'],
            features['speechiness'],
            features['tempo'],
            features['time_signature'],
            features['valence']
        ))

        cur.execute("INSERT OR IGNORE INTO UserTracks VALUES (?,?,?)", (
            track['id'],
            USER,
            item['added_at']
        ))

        album = sp.album(track['album']['id'])
        cur.execute("INSERT OR IGNORE INTO Albums VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
            album['id'],
            album['album_type'],
            album['total_tracks'],
            album['images'][0]['url'] if album['images'] else None,
            album['name'],
            album['release_date'],
            album['release_date_precision'],
            album['uri'],
            ','.join(c['type'] + '' + c['text'] for c in album['copyrights']),
            album['label'],
            album['popularity']
        ))

        for artist_id in [a['id'] for a in track['artists']]:
            artist = sp.artist(artist_id)
            cur.execute("INSERT OR IGNORE INTO Artists VALUES (?,?,?,?,?)", (
                artist['id'],
                artist['images'][0]['url'] if artist['images'] else None,
                artist['name'],
                artist['popularity'],
                artist['uri']
            ))

            cur.execute("INSERT OR IGNORE INTO AlbumArtists VALUES (?,?)", (
                album['id'],
                artist['id']
            ))

            cur.execute("INSERT OR IGNORE INTO TrackArtists VALUES (?,?)", (
                track['id'],
                artist['id']
            ))

            for genre in artist['genres']:
                cur.execute("INSERT OR IGNORE INTO Genres VALUES (?)", (genre,))
                cur.execute("INSERT OR IGNORE INTO ArtistGenres VALUES (?,?)", (
                    artist['id'],
                    genre
                ))
    con.commit()
    offset += LIMIT
    print(f'{offset} songs completed.')
    playlist = sp.current_user_saved_tracks(limit=LIMIT, offset=offset)
print(f'Done at ~{offset} songs')
con.close()
