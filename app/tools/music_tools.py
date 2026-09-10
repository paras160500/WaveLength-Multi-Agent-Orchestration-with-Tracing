# =========================================================================================
#                                     Import/Init Statements
# =========================================================================================

import ast 
from langchain_core.tools import tool 
from app.database import db 

# =========================================================================================
#                                        Tools Statements
# =========================================================================================

@tool
def get_album_by_artist(artist : str):
    """
        Get albums by an artist from the music database
    """
    return db.run(
        """
        SELECT Album.Title, Artist.Name
        FROM Album
        JOIN Artist ON Album.ArtistId = Artist.ArtistId
        WHERE Artist.Name LIKE '%{}%';
        """.format(artist),include_columns=True
    )


@tool
def get_tracks_by_artist(artist : str):
    """
        Get songs/tracks by an artist from the music database
    """
    return db.run(
        """
        SELECT Track.Name as SongName, Artist.Name as ArtistName
        FROM Album
        LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId
        LEFT JOIN Track ON Track.AlbumId = Album.AlbumId
        WHERE Artist.Name LIKE '%{}%';
        """.format(artist) , include_columns=True
    )


@tool
def get_songs_by_genre(genre : str):
    """
        Fetch songs from the database that match a specific genre, grouped by artist(max 8 length)
    """
    genre_id_query = f"SELECT GenreId FROM Genre WHERE Name LIKE '%{genre}%'"
    genre_ids = db.run(genre_id_query)

    if not genre_ids:
        return f"No Songs found for the genre : {genre}"

    genre_ids = ast.literal_eval(genre_ids)
    genre_id_list = ", ".join(str(gid[0]) for gid in genre_ids) 

    songs_query = f"""
        SELECT Track.Name as SongName, Artist.Name as ArtistName
        FROM Track
        LEFT JOIN Album ON Track.AlbumId = Album.AlbumId
        LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId
        WHERE Track.GenreId IN ({genre_id_list})
    """
    songs = db.run(songs_query , include_columns=True)

    if not songs:
        return f"No songs found for the genre: {genre}"

    formatted_songs = ast.literal_eval(songs)
    return [
        {"Song" : song['SongName'] , "Artist" : song['ArtistName']} for song in formatted_songs
    ]


@tool
def check_for_song(song_title : str):
    """
        Check if a song exists in the database by its name.
    """
    return db.run(
        f"SELECT * FROM Track WHERE Name LIKE '%{song_title}%';", include_columns=True
    )


music_tools = [get_album_by_artist , get_tracks_by_artist , get_songs_by_genre , check_for_song]