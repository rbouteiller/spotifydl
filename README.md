# spotifydl

## Description

This repository provides a Python script to download Spotify playlists, top tracks,liked tracks, recommendations, and search results as MP3 files, leveraging the Spotify and YouTube APIs.

## Features

1. Download songs from a chosen Spotify playlist.
2. Download recommended songs based on a Spotify playlist.
3. Download your top tracks from Spotify.
4. Download recommendations based on your top tracks.
5. Download liked(saved) tracks from your profile.
6. Create new Spotify playlists from recommendations or top tracks.
7. Search for tracks, artists, albums, and download songs from the search results.
8. Set the preferred quality of downloaded songs (190kbps or 320kbps).

## Dependencies

1. `tekore` - For accessing the Spotify API.
2. `yt-dlp` - For downloading and converting songs from YouTube.
3. `eyed3` - For editing ID3 tags (metadata) in the downloaded MP3 files.
4. `urllib` - For fetching album artwork.

## Setup and Usage

1. **Spotify Developer Dashboard** From the Spotify Developer Dashboard create a new app with redirect url `http://localhost:5000/`

3. **API Keys:** Replace `client_id`, `client_secret` with your personal credentials from the new app created.
4. **FFMEG Location:** Replace `YOUR_FFMEG_LOCATION_HERE` with your ffmeg.exe location( modified because requesting the exe location in code caused a bunch of issues for me)

5. **Install Dependencies:**

```bash
pip install tekore yt-dlp eyed3
```

3. **Run Script:**

```bash
python spotify.py
```

Replace `spotify.py` with the name of the Python script if different.

4. **Follow On-Screen Prompts:** 
Upon your initial launch, a browser window will open, prompting a connection to your Spotify account. Note that this doesn't have to be the same account linked to the API. The script offers a menu-driven interface to navigate its multiple features. Simply select your preferred function and adhere to the displayed guidelines.
The script then provides a menu-driven interface for various functionalities. Choose the desired operation and follow the on-screen instructions.

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
