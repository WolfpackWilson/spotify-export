CREATE TABLE Tracks
(
    id          TEXT PRIMARY KEY,
    album_id    TEXT NOT NULL,
    disc_number INTEGER,
    duration    INTEGER,
    explicit    INTEGER,
    isrc        TEXT,
    name        TEXT,
    popularity  INTEGER,
    preview     TEXT,
    uri         TEXT,
    FOREIGN KEY (album_id) REFERENCES Albums (id)
);
CREATE TABLE AudioFeatures
(
    id               TEXT PRIMARY KEY,
    acousticness     REAL,
    danceability     REAL,
    energy           REAL,
    instrumentalnees REAL,
    key              INTEGER,
    liveness         REAL,
    loudness         REAL,
    mode             INTEGER,
    speechiness      REAL,
    tempo            REAL,
    time_signature   INTEGER,
    valence          REAL,
    FOREIGN KEY (id) REFERENCES Tracks (id)
);
CREATE TABLE Albums
(
    id                     TEXT PRIMARY KEY,
    album_type             TEXT,
    total_tracks           INTEGER,
    image_url              TEXT,
    name                   TEXT,
    release_date           TEXT,
    release_date_precision TEXT,
    uri                    TEXT,
    copyrights             TEXT,
    label                  TEXT,
    popularity             INTEGER
);
CREATE TABLE Artists
(
    id         TEXT PRIMARY KEY,
    image_url  TEXT,
    name       TEXT,
    popularity INTEGER,
    uri        TEXT
);
CREATE TABLE UserTracks
(
    track_id TEXT NOT NULL,
    added_by TEXT,
    added_at TEXT,
    PRIMARY KEY (track_id, added_by),
    FOREIGN KEY (track_id) REFERENCES Tracks (id)
);
CREATE TABLE Genres
(
    genre TEXT PRIMARY KEY
);
CREATE TABLE AlbumArtists
(
    album_id  TEXT,
    artist_id TEXT,
    PRIMARY KEY (album_id, artist_id),
    FOREIGN KEY (album_id) REFERENCES Albums (id),
    FOREIGN KEY (artist_id) REFERENCES Artists (id)
);
CREATE TABLE TrackArtists
(
    track_id  TEXT,
    artist_id TEXT,
    PRIMARY KEY (track_id, artist_id),
    FOREIGN KEY (track_id) REFERENCES Tracks (id),
    FOREIGN KEY (artist_id) REFERENCES Artists (id)
);
CREATE TABLE ArtistGenres
(
    artist_id TEXT,
    genre     TEXT,
    PRIMARY KEY (artist_id, genre),
    FOREIGN KEY (artist_id) REFERENCES Artists (id),
    FOREIGN KEY (genre) REFERENCES Genres (genre)
)
