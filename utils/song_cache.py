import json
import os


CACHE_FILE = "songs_cache.json"


class SongCache:


    def __init__(self):

        self.data = {}

        self.load()



    def load(self):

        if os.path.exists(CACHE_FILE):

            with open(
                CACHE_FILE,
                encoding="utf-8"
            ) as file:

                self.data = json.load(file)

        else:

            self.data = {}



    def save(self):

        with open(
            CACHE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.data,
                file,
                indent=4,
                ensure_ascii=False
            )



    def get(
        self,
        category
    ):

        return self.data.get(
            category,
            []
        )



    def add(
        self,
        category,
        songs
    ):

        self.data[category] = songs

        self.save()

    def remove(
            self,
            category,
            song
    ):

        if category not in self.data:
            return

        self.data[category] = [
            s for s in self.data[category]
            if s["uri"] != song["uri"]
        ]

        self.save()