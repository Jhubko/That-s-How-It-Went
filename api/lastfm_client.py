import os
import requests
import random

from dotenv import load_dotenv


load_dotenv()



class LastFMClient:


    def __init__(self):

        self.api_key = os.getenv(
            "LASTFM_API_KEY"
        )

        self.url = (
            "https://ws.audioscrobbler.com/2.0/"
        )



    def get_tracks_by_tag(
            self,
            tag,
            limit=50
    ):


        params = {

            "method":
                "tag.gettoptracks",

            "tag":
                tag,

            "api_key":
                self.api_key,

            "format":
                "json",

            "limit":
                limit

        }


        response = requests.get(
            self.url,
            params=params,
            timeout=10
        )


        data = response.json()


        tracks = []


        try:

            for item in data["tracks"]["track"]:

                tracks.append({

                    "artist":
                        item["artist"]["name"],

                    "title":
                        item["name"]

                })


        except KeyError:

            return []



        return tracks



    def get_random_tracks(
            self,
            tag,
            amount=2
    ):


        tracks = self.get_tracks_by_tag(
            tag
        )


        if len(tracks) < amount:

            return tracks


        return random.sample(
            tracks,
            amount
        )