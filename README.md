# That's How It Went

An application inspired by music quiz shows, where players have to complete missing parts of song lyrics.

The application provides a separate player screen and a host panel that controls the entire game flow.

## Features

- Music category selection
- Random song selection from chosen categories
- Spotify-based song playback
- Lyrics fetching and synchronization
- Automatic song stopping at a random point
- Completing missing lyrics
- Checking player answers
- Local cache system for downloaded songs
- Ability to download additional songs
- Separate player display and host control panel

## Views

### Host Panel

Allows the host to:
- select a music category,
- choose a song,
- start a round,
- stop playback,
- reveal answers,
- manage the available song database.

### Player Screen

Displays:
- currently playing lyrics,
- the next line of the song,
- input fields for missing words,
- answer results.

## Technologies

- Python
- PySide6
- Spotify API
- Last.fm API
- LRCLib API
- JSON-based local cache system
