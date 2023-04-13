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
    with open('.\\instances\\create_table.sql') as f:
        cur.executescript(f.read())
        con.commit()

offset = STARTING_OFFSET
playlist = sp.current_user_saved_tracks(limit=LIMIT, offset=offset)
print(f'{offset} songs completed')
while playlist['items']:
    for item in playlist['items']:
        cur.execute("INSERT OR IGNORE INTO UserTracks VALUES (?,?,?)", (
            item['track']['id'],
            USER,
            item['added_at']
        ))

    tracks = [item['track'] for item in playlist['items']]
    for track in tracks:
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

    track_ids = [track['id'] for track in tracks]
    features_lst = sp.audio_features(track_ids)
    for features in features_lst:
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

    album_ids = [track['album']['id'] for track in tracks]
    albums_lst = sp.albums(album_ids)['albums']
    for album in albums_lst:
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

    artists_info = [
        (track['artists'][i]['id'], track['id'], track['album']['id'])
        for track in tracks
        for i in range(len(track['artists']))
    ]

    artists = sp.artists(a[0] for a in artists_info)
    for idx, artist in enumerate(artists["artists"]):
        cur.execute("INSERT OR IGNORE INTO Artists VALUES (?,?,?,?,?)", (
            artist['id'],
            artist['images'][0]['url'] if artist['images'] else None,
            artist['name'],
            artist['popularity'],
            artist['uri']
        ))

        album_id = artists_info[idx][2]
        cur.execute("INSERT OR IGNORE INTO AlbumArtists VALUES (?,?)", (
            album_id,
            artist['id']
        ))

        track_id = artists_info[idx][1]
        cur.execute("INSERT OR IGNORE INTO TrackArtists VALUES (?,?)", (
            track_id,
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
con.commit()
con.close()
