CREATE TABLE Tracks
(
    id          TEXT PRIMARY KEY,
    album_id    TEXT    NOT NULL,
    disc_number INTEGER NOT NULL,
    duration    INTEGER NOT NULL,
    explicit    INTEGER NOT NULL,
    isrc        TEXT,
    name        TEXT    NOT NULL,
    popularity  INTEGER NOT NULL,
    preview     TEXT    NOT NULL,
    uri         TEXT    NOT NULL,
    FOREIGN KEY (album_id) REFERENCES Albums (id)
);
CREATE TABLE AudioFeatures
(
    id               TEXT PRIMARY KEY,
    acousticness     REAL    NOT NULL,
    danceability     REAL    NOT NULL,
    energy           REAL    NOT NULL,
    instrumentalnees REAL    NOT NULL,
    key              INTEGER NOT NULL,
    liveness         REAL    NOT NULL,
    loudness         REAL    NOT NULL,
    mode             INTEGER NOT NULL,
    speechiness      REAL    NOT NULL,
    tempo            REAL    NOT NULL,
    time_signature   INTEGER NOT NULL,
    valence          REAL    NOT NULL,
    FOREIGN KEY (id) REFERENCES Tracks (id)
);
CREATE TABLE Albums
(
    id                     TEXT PRIMARY KEY,
    album_type             TEXT    NOT NULL,
    total_tracks           INTEGER NOT NULL,
    image_url              TEXT,
    name                   TEXT    NOT NULL,
    release_date           TEXT    NOT NULL,
    release_date_precision TEXT    NOT NULL,
    uri                    TEXT    NOT NULL,
    copyrights             TEXT    NOT NULL,
    label                  TEXT    NOT NULL,
    popularity             INTEGER NOT NULL
);
CREATE TABLE Artists
(
    id         TEXT PRIMARY KEY,
    image_url  TEXT,
    name       TEXT    NOT NULL,
    popularity INTEGER NOT NULL,
    uri        TEXT    NOT NULL
);
CREATE TABLE UserTracks
(
    track_id TEXT NOT NULL,
    added_by TEXT NOT NULL,
    added_at TEXT NOT NULL,
    PRIMARY KEY (track_id, added_by),
    FOREIGN KEY (track_id) REFERENCES Tracks (id)
);
CREATE TABLE Genres
(
    genre TEXT PRIMARY KEY
);
CREATE TABLE AlbumArtists
(
    album_id  TEXT NOT NULL,
    artist_id TEXT NOT NULL,
    PRIMARY KEY (album_id, artist_id),
    FOREIGN KEY (album_id) REFERENCES Albums (id),
    FOREIGN KEY (artist_id) REFERENCES Artists (id)
);
CREATE TABLE TrackArtists
(
    track_id  TEXT NOT NULL,
    artist_id TEXT NOT NULL,
    PRIMARY KEY (track_id, artist_id),
    FOREIGN KEY (track_id) REFERENCES Tracks (id),
    FOREIGN KEY (artist_id) REFERENCES Artists (id)
);
CREATE TABLE ArtistGenres
(
    artist_id TEXT NOT NULL,
    genre     TEXT NOT NULL,
    PRIMARY KEY (artist_id, genre),
    FOREIGN KEY (artist_id) REFERENCES Artists (id),
    FOREIGN KEY (genre) REFERENCES Genres (genre)
)
