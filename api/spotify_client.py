import os

import spotipy

from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv

load_dotenv()

class SpotifyClient:


    def __init__(self):

        self.spotify = spotipy.Spotify(

            auth_manager=SpotifyOAuth(

                client_id=os.getenv(
                    "SPOTIFY_CLIENT_ID"
                ),

                client_secret=os.getenv(
                    "SPOTIFY_CLIENT_SECRET"
                ),

                redirect_uri=os.getenv(
                    "SPOTIFY_REDIRECT_URI"
                ),

                scope=
                """
                user-read-playback-state
                user-modify-playback-state
                user-read-currently-playing
                """
            )
        )

    def search_song(
            self,
            artist,
            title
    ):


        result = self.spotify.search(

            q=f'artist:{artist} track:{title}',

            type="track",

            limit=5
        )


        tracks = result["tracks"]["items"]


        if not tracks:

            return None

        track = tracks[0]

        return {


            "id":
                track["id"],


            "uri":
                track["uri"],


            "name":
                track["name"],


            "artist":
                track["artists"][0]["name"],


            "url":
                track["external_urls"]["spotify"]

        }

    def convert_lastfm_tracks(
            self,
            tracks
    ):


        result = []


        for song in tracks:


            spotify_song = self.search_song(

                song["artist"],

                song["title"]

            )


            if spotify_song:

                result.append(
                    spotify_song
                )


        return result

    def play(self, uri):

        devices = self.spotify.devices()

        active_device = None

        for device in devices["devices"]:

            if device["is_active"]:
                active_device = device["id"]

                break

        if not active_device:
            print(
                "Brak aktywnego urządzenia Spotify"
            )

            return

        self.spotify.start_playback(

            device_id=active_device,

            uris=[
                uri
            ]

        )


    def pause(self):

        self.spotify.pause_playback()


    def resume(self):

        self.spotify.start_playback()

    def stop(self):

        self.spotify.pause_playback()

    def devices(self):

        return self.spotify.devices()

    def get_progress(self):

        playback = self.spotify.current_playback()

        if playback and playback["is_playing"]:
            return playback["progress_ms"]

        return None