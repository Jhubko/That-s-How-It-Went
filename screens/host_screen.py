import random

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout
)

from PySide6.QtCore import QTimer

from core.game_manager import game

from api.lrclib import LRCLib
from api.lastfm_client import LastFMClient
from api.spotify_client import SpotifyClient

from utils.lyrics_parser import parse_lrc
from utils.song_cache import SongCache

class HostScreen(QWidget):

    def __init__(self, main):

        super().__init__()

        self.main = main

        self.lyrics_api = LRCLib()
        self.lastfm = LastFMClient()
        self.spotify = SpotifyClient()

        self.cache = SongCache()

        self.game_timer = QTimer()

        self.game_timer.timeout.connect(
            self.update_game
        )

        self.categories = [

            "polish music",
            "polish music",
            "polish rock",
            "polish pop",
            "polish hip hop",
            "disco polo",

            "rock",
            "classic rock",
            "pop rock",
            "alternative rock",
            "punk rock",
            "indie rock",

            "pop",
            "dance pop",
            "80s pop",
            "90s pop",
            "2000s",

            "dance",
            "disco",
            "party",
            "eurodance",

            "metal",
            "heavy metal",
            "nu metal",

            "80s",
            "90s",
            "classic hits",
            "one hit wonders",
            "oldies"
        ]


        layout = QVBoxLayout()

        self.info = QLabel(
            "Panel prowadzącego"
        )

        self.buttons_layout = QVBoxLayout()

        self.category_button = QPushButton(
            "POKAŻ KATEGORIE"
        )

        self.download_button = QPushButton(
            "POBIERZ WIĘCEJ PIOSENEK"
        )

        self.download_button.clicked.connect(
            self.download_more_songs
        )

        self.download_button.hide()

        self.category_button.clicked.connect(
            self.show_categories
        )

        self.action_button = QPushButton(
            "START RUNDY"
        )

        self.action_button.clicked.connect(
            self.action_clicked
        )

        self.check_button = QPushButton(
            "POKAŻ ODPOWIEDŹ"
        )

        self.check_button.clicked.connect(
            self.show_answer
        )

        layout.addWidget(
            self.info
        )

        self.continue_button = QPushButton(
            "KONTYNUUJ PIOSENKĘ"
        )

        self.continue_button.clicked.connect(
            self.continue_song
        )

        self.continue_button.hide()

        layout.addWidget(
            self.category_button
        )

        layout.addWidget(
            self.download_button
        )

        layout.addWidget(
            self.continue_button
        )

        layout.addLayout(
            self.buttons_layout
        )


        layout.addWidget(
            self.action_button
        )


        layout.addWidget(
            self.check_button
        )


        self.setLayout(
            layout
        )

    def clear_buttons(self):

        while self.buttons_layout.count():

            item = self.buttons_layout.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()

    def show_categories(self):

        self.reset_game()
        self.clear_buttons()

        selected_categories = random.sample(
            self.categories,
            min(2, len(self.categories))
        )

        game.categories = selected_categories


        self.main.player_screen.show_categories(
            selected_categories
        )


        for category in selected_categories:


            button = QPushButton(
                category.upper()
            )


            button.clicked.connect(
                lambda checked=False, c=category:
                self.choose_category(c)
            )


            self.buttons_layout.addWidget(
                button
            )


        self.info.setText(
            "Wybierz kategorię"
        )

    def choose_category(self, category):

        self.clear_buttons()

        game.category = category

        self.info.setText(
            "Pobieranie piosenek..."
        )

        songs = self.cache.get(
            category
        )

        if not songs:
            tracks = self.lastfm.get_random_tracks(
                category,
                30
            )

            songs = self.spotify.convert_lastfm_tracks(
                tracks
            )

            self.cache.add(
                category,
                songs
            )

        songs = random.sample(
            songs,
            min(2, len(songs))
        )

        game.songs = songs

        self.main.player_screen.show_songs(
            songs
        )

        for song in songs:
            button = QPushButton(
                f"{song['artist']} - {song['name']}"
            )

            button.clicked.connect(
                lambda checked=False, s=song:
                self.choose_song(s)
            )

            self.buttons_layout.addWidget(
                button
            )

        self.info.setText(
            f"Kategoria: {category}"
        )

        self.download_button.show()

    def choose_song(self, song):

        game.song = song
        game.song_used = False

        self.info.setText(
            f"Wybrano:\n"
            f"{song['artist']} - {song['name']}"
        )


        self.main.player_screen.show_song(
            song
        )

    def action_clicked(self):

        if not game.song:

            self.info.setText(
                "Najpierw wybierz piosenkę!"
            )

            return


        if game.music_playing:

            self.stop_round()

        else:

            self.start_round()



    def start_round(self):

        self.clear_buttons()
        self.continue_button.hide()
        self.stop_used = False

        lyrics = self.lyrics_api.get_lyrics(
            game.song["artist"],
            game.song["name"]
        )


        if not lyrics:

            self.info.setText(
                "Nie znaleziono tekstu"
            )

            return

        game.full_lyrics = parse_lrc(
            lyrics
        )

        game.selected_line = None
        game.selected_line_index = None

        self.choose_stop_time()

        stop_seconds = int(
            game.stop_time / 1000
        )

        minutes = stop_seconds // 60
        seconds = stop_seconds % 60

        self.spotify.play(
            game.song["uri"]
        )


        game.music_playing = True


        self.game_timer.start(
            200
        )


        self.action_button.setText(
            "STOP"
        )

        self.info.setText(
            f"Runda trwa...\n"
            f"STOP: {minutes}:{seconds:02d}\n\n"
            f"Brakujący tekst:\n"
            f"{game.selected_line['text']}"
        )


    def update_game(self):

        if not game.music_playing:
            return

        progress = self.spotify.get_progress()

        if progress is None:
            return


        if progress >= game.stop_time and not self.continue_button.isVisible() and not game.stop_used:
            game.stop_used = True
            self.stop_round()

            return

        current = ""
        next_line = ""

        current_index = None

        for i, line in enumerate(game.full_lyrics):

            if progress >= line["time"]:
                current = line["text"]
                current_index = i

        if current_index is not None and current_index + 1 < len(game.full_lyrics):

            next_index = current_index + 1

            next_line = game.full_lyrics[next_index]["text"]

            if next_index == game.selected_line_index:
                next_line = hide_line(
                    next_line
                )

        self.main.player_screen.show_current_lyrics(
            current,
            next_line
        )

    def stop_round(self):

        self.game_timer.stop()

        self.spotify.pause()

        game.music_playing = False

        self.action_button.setText(
            "START RUNDY"
        )

        if game.selected_line:
            self.info.setText(
                f"Muzyka zatrzymana\n\n"
                f"Brakujący tekst:\n"
                f"{game.selected_line['text']}"
            )

            self.main.player_screen.show_guess_fields(
                game.selected_line["text"]
            )

        self.continue_button.show()

    def show_answer(self):

        if not game.selected_line:
            return

        self.main.player_screen.show_guess_result(
            game.selected_line["text"].split()
        )

        if (
                game.song
                and game.category
                and not game.song_used
        ):
            self.cache.remove(
                game.category,
                game.song
            )

            game.song_used = True

    def choose_stop_time(self):

        possible_lines = []

        if not game.full_lyrics:
            game.stop_time = 90000
            game.selected_line = None
            game.selected_line_index = None
            return

        # długość tekstu/piosenki z ostatniej linijki

        song_length = game.full_lyrics[-1]["time"]

        # maksymalny czas zatrzymania
        max_time = int(
            song_length * 0.7
        )

        for index, line in enumerate(game.full_lyrics):

            if (
                    line["time"] >= 30000
                    and line["time"] <= max_time
                    and len(line["text"].split()) >= 3
            ):
                possible_lines.append(
                    (index, line)
                )

        if not possible_lines:
            possible_lines = [
                (i, line)
                for i, line in enumerate(game.full_lyrics)
                if line["time"] >= 30000
            ]

        index, selected = random.choice(
            possible_lines
        )

        game.selected_line = selected

        game.selected_line_index = index

        game.stop_time = selected["time"] - 1000

        seconds = int(
            game.stop_time / 1000
        )

        minutes = seconds // 60
        seconds = seconds % 60

        self.info.setText(
            f"Runda trwa...\n"
            f"STOP: {minutes}:{seconds:02d}\n\n"
            f"Brakujący tekst:\n"
            f"{selected['text']}"
        )

        print(
            "STOP:",
            game.stop_time / 1000,
            "sek"
        )

    def continue_song(self):

        self.spotify.resume()

        game.music_playing = True

        self.continue_button.hide()

        self.info.setText(
            "Piosenka kontynuowana"
        )

        self.game_timer.start(
            200
        )

    def reset_game(self):

        self.spotify.pause()

        self.game_timer.stop()

        game.category = None
        game.song = None
        game.songs = []
        game.full_lyrics = []
        game.selected_line = None
        game.selected_line_index = None
        game.stop_time = 0
        game.music_playing = False
        game.stop_used = False
        game.song_used = False

        self.continue_button.hide()
        self.download_button.hide()

        self.action_button.setText(
            "START RUNDY"
        )

        self.info.setText(
            "Panel prowadzącego"
        )

        self.clear_buttons()

        self.main.player_screen.clear()

    def download_more_songs(self):

        if not game.category:
            return

        self.info.setText(
            "Pobieranie dodatkowych piosenek..."
        )

        tracks = self.lastfm.get_random_tracks(
            game.category,
            30
        )

        songs = self.spotify.convert_lastfm_tracks(
            tracks
        )

        current = list(
            self.cache.get(game.category)
        )

        existing_ids = {
            song["uri"]
            for song in current
        }

        new_songs = [
            song
            for song in songs
            if song["uri"] not in existing_ids
        ]

        current.extend(
            new_songs
        )

        self.cache.add(
            game.category,
            current
        )

        self.info.setText(
            f"Dodano {len(new_songs)} nowych piosenek"
        )

def hide_line(text):

    result = []


    for word in text.split():

        clean = word.strip(
            ".,!?;:"
        )


        result.append(
            "_" * len(clean)
        )


    return " ".join(result)
