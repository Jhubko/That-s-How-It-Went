import requests


class LRCLib:

    BASE_URL = "https://lrclib.net/api/search"

    def get_lyrics(self, artist, title):

        try:

            response = requests.get(
                self.BASE_URL,
                params={
                    "artist_name": artist,
                    "track_name": title
                },
                timeout=(5, 30)
            )

            response.raise_for_status()

            data = response.json()

            if not data:
                return None

            for item in data:

                if item.get("syncedLyrics"):
                    return item["syncedLyrics"]

            return data[0].get("plainLyrics")


        except requests.exceptions.Timeout:

            print("LRCLIB: przekroczono czas oczekiwania")
            return None


        except Exception as e:

            print("LRCLIB error:", e)
            return None