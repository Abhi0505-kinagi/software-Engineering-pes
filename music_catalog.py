import pickle
import random
import sqlite3

try:
    conn = sqlite3.connect(":memory:")
    print("Database connected successfully!")

except sqlite3.Error as e:
    print(f"Database error: {e}")
conn.execute('''CREATE TABLE songs
            (id INTEGER PRIMARY KEY, title TEXT,
            artist TEXT, plays INTEGER)''')


def add_song(title, artist, plays=0, playlist=None):
    """Add a song to the database and playlist."""
    if playlist is None:
        playlist = []
    conn.execute('''INSERT INTO songs (title, artist, plays)
                 VALUES (?, ?, ?)''', (title, artist, plays))
    playlist.append(title)
    return playlist


def shuffle_pick():
    """Return a random song ID or None if empty."""
    ids = [r[0] for r in conn.execute("SELECT id FROM songs")]
    return random.choice(ids) if ids else None


def popularity(title):
    """Return the song's popularity category."""
    row = conn.execute('''SELECT plays FROM songs WHERE title = ?''',
                       (title,)).fetchone()
    if row is None:
        return "unknown"
    return "popular" if row[0] > 100 else "niche"


def save_playlist(playlist):
    """Serialize the playlist using pickle."""
    return pickle.dumps(playlist)


def load_playlist(blob):
    """Deserialize a playlist from pickle data."""
    return pickle.loads(blob)


def total_plays():
    """Return the total plays of all songs."""
    try:
        result = conn.execute(
            "SELECT SUM(plays) FROM songs"
        ).fetchone()[0]
        return result if result is not None else 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 0


def main():
    """Run the playlist management demonstration."""
    pl = add_song("Aurora", "Nila", 250)
    add_song("Monsoon", "Kavya", 40, pl)
    blob = save_playlist(pl)
    load = load_playlist(blob)
    if len(load) > 1:
        print("multi-song playlist")
    print(popularity("Aurora"), popularity("Monsoon"),
          shuffle_pick(), total_plays())


main()
