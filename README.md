# spotifydl

## Description

This repository provides a Python script to download Spotify playlists, top tracks, recommendations, and search results as MP3 files, leveraging the Spotify and YouTube APIs.

## Features

1. Download songs from a chosen Spotify playlist.
2. Download recommended songs based on a Spotify playlist.
3. Download your top tracks from Spotify.
4. Download recommendations based on your top tracks.
5. Create new Spotify playlists from recommendations or top tracks.
6. Search for tracks, artists, albums, and download songs from the search results.
7. Set the preferred quality of downloaded songs (190kbps or 320kbps).

## Dependencies

1. `tekore` - For accessing the Spotify API.
2. `yt_dlp` - For downloading and converting songs from YouTube.
3. `eyed3` - For editing ID3 tags (metadata) in the downloaded MP3 files.
4. `urllib` - For fetching album artwork.

## Setup and Usage

1. **API Keys:** Replace `client_id`, `client_secret`, and `redirect_uri` with your personal credentials from the Spotify Developer Dashboard.

2. **Install Dependencies:**

```bash
pip install tekore yt_dlp eyed3
```

3. **Run Script:**

```bash
python script_name.py
```

Replace `script_name.py` with the name of the Python script if different.

4. **Follow On-Screen Prompts:** The script provides a menu-driven interface for various functionalities. Choose the desired operation and follow the on-screen instructions.

## Security Warning

Do not share or publish your `client_id` and `client_secret` publicly. This script uses them to authenticate and access your Spotify data. 

## Limitations

1. Songs are sourced from YouTube, so some tracks may differ slightly from the original Spotify version.
2. Some tracks might not be available or might not be downloaded due to various reasons such as unavailability on YouTube.

## Disclaimer

Downloading copyrighted songs without permission is illegal in many countries. This script is intended for educational purposes and personal use. Always respect copyright laws and terms of service of the platforms you interact with.

## Contribution

Feel free to contribute to this project by opening issues or submitting pull requests. 

## License

This project is licensed under the MIT License. Refer to the LICENSE file for more details.
