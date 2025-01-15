# Download spotify playlist to mp3

import tekore as tk
import os
import yt_dlp as youtube_dl
import eyed3
import urllib
# import vlc

# Spotify API
client_id = 'YOUR_CLIENT_ID_HERE'
client_secret = 'YOUR_CLIENT_SECRET_HERE'

redirect_uri = 'http://localhost:5000/'

user_token = None
# Read user_token from file if it exists
if os.path.exists('user_token.txt'):
    with open('user_token.txt', 'r') as f:
        user_token = f.read()

# Test token if it is valid
try:
    spotify = tk.Spotify(user_token)
    spotify.current_user()
except tk.HTTPError:
    # If token is invalid, get new token
    user_token = tk.prompt_for_user_token(
        client_id,
        client_secret,
        redirect_uri,
        scope=tk.scope.every
    )
    # Save user_token in a file
    with open('user_token.txt', 'w') as f:
        f.write(str(user_token))
    spotify = tk.Spotify(user_token)

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'ffmpeg_location': 'YOUR_FFMEG_LOCATION_HERE',
    'format': 'bestaudio/best',
    'extractaudio': True,
    'outtmpl': '%(title)s.%(ext)s',
    'addmetadata': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'logger': MyLogger(),
    # 'progress_hooks': [my_hook],
}


def get_yt_track_url(track):
    # Get youtube url of song
    song = track.name
    artist = track.artists[0].name
    print('Searching: ' + song + ' by ' + artist)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info('ytsearch1:' + song + ' ' + artist, download=False)['entries'][0]
            return result['webpage_url']
        except:
            return None

def songs_downloader(folder, tracks):
    # Download songs
    for i, track in enumerate(tracks):
        print(f"Tracks downloaded: {i}/{len(tracks)}")
        song = track.name
        artist = track.artists[0].name
        album = track.album.name

        # Sanitize names
        song = sanitize_filename(song)
        artist = sanitize_filename(artist)
        album = sanitize_filename(album)

        print(f'Downloading: {song} by {artist}')
        ydl_opts['outtmpl'] = f'{artist} - {song}.%(ext)s'

        # Build the destination path
        destination_path = os.path.join(folder, artist, album)
        file_name = f'{artist} - {song}.mp3'
        full_destination = os.path.join(destination_path, file_name)

        # Download song if not already downloaded
        if not os.path.exists(full_destination):
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f'ytsearch1:{song} {artist}'])

                # If song is not downloaded, skip
                if not os.path.exists(file_name):
                    print(f'Failed to download {file_name}')
                    continue

                # Add metadata
                audiofile = eyed3.load(file_name)
                if audiofile.tag is None:
                    audiofile.initTag()
                audiofile.tag.artist = artist
                audiofile.tag.title = song
                audiofile.tag.album = album
                audiofile.tag.album_artist = track.album.artists[0].name

                # Get the artist's genre
                artist_id = track.artists[0].id
                genres = spotify.artist(artist_id).genres
                if genres:
                    audiofile.tag.genre = genres[-1]
                audiofile.tag.track_num = track.track_number

                # Add album art
                imagedata = urllib.request.urlopen(track.album.images[0].url).read()
                audiofile.tag.images.set(3, imagedata, 'image/jpeg')
                audiofile.tag.save()

                # Create destination directories
                os.makedirs(destination_path, exist_ok=True)

                # Move song to destination folder
                try:
                    os.rename(file_name, full_destination)
                    print(f'Moved {file_name} to {full_destination}')
                except Exception as e:
                    print(f'Error moving file: {e}')
            except youtube_dl.utils.DownloadError as e:
                print(f"Error downloading '{song}' by '{artist}': {e}. Skipping this song.")
                continue
            except Exception as e:
                print(f"An unexpected error occurred while downloading '{song}' by '{artist}': {e}. Skipping this song.")
                continue
        else:
            print('Already downloaded')



print("Logged in as " + spotify.current_user().email)

def choose_quality():
    # Choose quality of songs
    quality = input("Choose quality of songs (190 or 320): ")
    if quality == '':
        ydl_opts['postprocessors'][0]['preferredquality'] = '320'
    elif quality == '190':
        ydl_opts['postprocessors'][0]['preferredquality'] = '190'
    elif quality == '320':
        ydl_opts['postprocessors'][0]['preferredquality'] = '320'
    else:
        print("Invalid input")
        choose_quality()


def list_playlists():
    playlists = spotify.playlists(spotify.current_user().id)
    for i, playlist in enumerate(playlists.items):
        print(i, end=". ")
        print(playlist.name)
    return playlists

def get_playlist_tracks(playlist):
    tracks = []
    playlist_uri = playlist.uri.split(":")[-1]
    results = spotify.playlist_items(playlist_uri)
    tracks.extend(results.items)
    while results.next:
        results = spotify.next(results)
        tracks.extend(results.items)
    return tracks
def list_liked_songs():
    liked_songs = []
    results = spotify.saved_tracks()
    liked_songs.extend(results.items)
    while results.next:
        results = spotify.next(results)
        liked_songs.extend(results.items)
    return liked_songs


    
def get_recommendations(tracks):
    track_ids = [t.track.id for t in tracks]
    recommendations = spotify.recommendations(track_ids=track_ids).tracks
    return recommendations

def get_top_tracks(limit=5):
    top_tracks = spotify.current_user_top_tracks(limit=limit).items
    return top_tracks

def create_playlist(name, description):
    user = spotify.current_user()
    playlist = spotify.playlist_create(
        user.id,
        name,
        public=False,
        description=description
    )
    return playlist

def add_tracks_to_playlist(playlist, tracks):
    uris = [t.uri for t in tracks]
    spotify.playlist_add(playlist.id, uris=uris)

def menu():
    print("1. Download songs from playlist")
    print("2. Download songs from recommendations")
    print("3. Download songs from top tracks")
    print("4. Download songs from top tracks recommendations")
    print("5. Create playlist from recommendations")
    print("6. Create playlist from top tracks")
    print("7. Create playlist from top tracks recommendations")
    print("8. Search")
    print("9. Exit")
    print("Extra options:")
    print("10. Choose quality of songs")
    print("11. Download liked songs")  # New option for downloading liked songs
    return int(input("Enter option: "))


def playlist_tracks_to_tracks(playlist_tracks):
    tracks = []
    for playlist_track in playlist_tracks:
        tracks.append(playlist_track.track)
    return tracks

def search(query, types=('track', 'artist', 'album')):
    results = spotify.search(query, types=types, limit=10)
    return results

def search_tracks(query):
    results = search(query, types=('track',))
    return results

def search_artists(query):
    results = search(query, types=('artist',))
    return results

def search_albums(query):
    results = search(query, types=('album',))
    return results

def search_playlists(query):
    results = search(query, types=('playlist',))
    return results

def search_menu():
    print("1. Search tracks")
    print("2. Search artists")
    print("3. Search albums")
    print("4. Exit")
    action = int(input("Enter option: "))
    if action == 1:
        query = input("Enter query: ")
        results = search_tracks(query)
        for i, track in enumerate(results[0].items):
            print(i, end=". ")
            print(track.name, end=" - ")
            print(track.artists[0].name)
        return query, results[0].items
    elif action == 2:
        query = input("Enter query: ")
        results = search_artists(query)
        for i, artist in enumerate(results[0].items):
            print(i, end=". ")
            print(artist.name)
        return query, results[0].items
    elif action == 3:
        query = input("Enter query: ")
        results = search_albums(query)
        for i, album in enumerate(results[0].items):
            print(i, end=". ")
            print(album.name, end=" - ")
            print(album.artists[0].name)
        return query, results[0].items
    elif action == 4:
        return None
    
def post_search_menu(query, results):
    print()
    print("1. Download songs from search results")
    print("2. Create playlist from search results")
    print("3. Exit")
    action = int(input("Enter option: "))
    if action == 1:
        # Choose song to download (one or more)
        songs_index = input("Enter songs number, all for all: ")
        if songs_index == 'all':
            songs_downloader("Search : "+query, results)
        else:
            # Split could be a , a space , a . or a -
            songs_index = songs_index.replace(',', ' ').replace('.', ' ').replace('-', ' ').split()
            songs_index = [int(i) for i in songs_index]
            songs_downloader("Search : "+query, [results[i] for i in songs_index])
    elif action == 2:
        playlist = create_playlist(query, "Created by spotify-downloader")
        add_tracks_to_playlist(playlist, results)
        print("Playlist created: " + playlist.name)
    elif action == 3:
        return

def main():
    while True:
        action = menu()
        if action == 1:
            playlists = list_playlists()
            playlist = playlists.items[int(input("Enter playlist number: "))]
            tracks = get_playlist_tracks(playlist)
            tracks = playlist_tracks_to_tracks(tracks)
            songs_downloader(playlist.name, tracks)
        elif action == 2:
            playlists = list_playlists()
            playlist = playlists.items[int(input("Enter playlist number: "))]
            tracks = get_playlist_tracks(playlist)
            recommendations = get_recommendations(tracks)
            songs_downloader(playlist.name+" recommendations", recommendations)
        elif action == 3:
            top_tracks = get_top_tracks(int(input("Enter number of top tracks: ")))
            songs_downloader("Top tracks", top_tracks)
        elif action == 4:
            top_tracks = get_top_tracks(int(input("Enter number of top tracks: ")))
            recommendations = get_recommendations(top_tracks)
            songs_downloader("Top tracks recommendations", recommendations)
        elif action == 5:
            playlists = list_playlists()
            playlist = playlists.items[int(input("Enter playlist number: "))]
            tracks = get_playlist_tracks(playlist)
            recommendations = get_recommendations(tracks)
            playlist = create_playlist(playlist.name + " recommendations", "Recommended songs from " + playlist.name)
            add_tracks_to_playlist(playlist, recommendations)
        elif action == 6:
            top_tracks = get_top_tracks()
            playlist = create_playlist("Top tracks", "Top tracks from user")
            add_tracks_to_playlist(playlist, top_tracks)
        elif action == 7:
            top_tracks = get_top_tracks()
            recommendations = get_recommendations(top_tracks)
            playlist = create_playlist("Top tracks recommendations", "Recommended songs from top tracks")
            add_tracks_to_playlist(playlist, recommendations)
        elif action == 8:
            search, results = search_menu()
            post_search_menu(search, results)
        elif action == 9:
            exit()
        elif action == 10:
            choose_quality()
        elif action == 11:  # New action for downloading liked songs
            liked_songs = list_liked_songs()
            liked_tracks = [item.track for item in liked_songs]
            songs_downloader("Liked songs", liked_tracks)




           

import time
import sys
if __name__ == "__main__":
    main()


