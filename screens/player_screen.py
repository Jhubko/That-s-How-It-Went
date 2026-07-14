from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QSizePolicy
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics

from utils.text_utils import normalize_word


class PlayerScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Tak To Leciało - Gracze"
        )

        self.resize(
            1200,
            700
        )

        layout = QVBoxLayout()


        # =========================
        # HEADER
        # =========================

        self.header_layout = QHBoxLayout()


        self.header = QLabel(
            "TAK TO LECIAŁO"
        )

        self.header.setStyleSheet("""
            font-size:48px;
            font-weight:bold;
        """)

        self.header.setAlignment(
            Qt.AlignCenter
        )

        self.header.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )


        self.header_layout.addWidget(
            self.header
        )

        self.header_layout.setAlignment(
            Qt.AlignCenter
        )


        layout.addLayout(
            self.header_layout
        )



        # =========================
        # TEKST AKTUALNY
        # =========================

        self.current_label = QLabel()

        self.current_label.setAlignment(
            Qt.AlignCenter
        )

        self.current_label.setWordWrap(
            True
        )

        self.current_label.setStyleSheet("""
            font-size:36px;
        """)


        layout.addWidget(
            self.current_label
        )



        # =========================
        # TEKST NASTĘPNY
        # =========================

        self.next_label = QLabel()

        self.next_label.setAlignment(
            Qt.AlignCenter
        )

        self.next_label.setWordWrap(
            True
        )

        self.next_label.setStyleSheet("""
            font-size:36px;
            color:lightgray;
        """)


        layout.addWidget(
            self.next_label
        )



        # =========================
        # ODPOWIEDZI
        # =========================

        self.guess_layout = QHBoxLayout()

        self.guess_layout.setAlignment(
            Qt.AlignCenter
        )

        layout.addLayout(
            self.guess_layout
        )


        self.guess_boxes = []


        self.setLayout(
            layout
        )



    # =========================
    # EKRANY
    # =========================

    def show_categories(self, categories):

        self.header.setText(
            "WYBIERZ KATEGORIĘ"
        )

        self.current_label.setText(
            "\n\n".join(
                category.upper()
                for category in categories
            )
        )

        self.next_label.clear()

        self.clear_guess_fields()



    def show_songs(self, songs):

        self.header.setText(
            "WYBIERZ PIOSENKĘ"
        )

        text = ""

        for index, song in enumerate(songs):

            text += (
                f"{index + 1}. "
                f"{song['artist']} - {song['name']}\n\n"
            )


        self.current_label.setText(
            text
        )

        self.next_label.clear()

        self.clear_guess_fields()



    def show_song(self, song):

        self.header.setText(
            "PRZYGOTUJ SIĘ!"
        )

        self.current_label.setText(
            song["artist"]
        )

        self.next_label.setText(
            song["name"]
        )

        self.clear_guess_fields()



    def show_current_lyrics(
            self,
            current_line,
            next_line
    ):

        self.header.setText(
            "ŚPIEWAJ!"
        )

        self.current_label.setText(
            current_line
        )

        self.next_label.setText(
            next_line
        )


        self.clear_guess_fields()



    def show_guess_fields(
            self,
            text
    ):

        self.next_label.clear()

        self.clear_guess_fields()


        for word in text.split():

            edit = QLineEdit()

            edit.setAlignment(
                Qt.AlignCenter
            )


            clean_word = normalize_word(
                word
            )


            edit.setPlaceholderText(
                "_" * len(clean_word)
            )


            metrics = QFontMetrics(
                edit.font()
            )


            width = (
                metrics.horizontalAdvance(
                    clean_word
                )
                + 60
            )


            edit.setFixedWidth(
                max(
                    width,
                    120
                )
            )

            edit.setFixedHeight(
                60
            )


            edit.setStyleSheet("""
                QLineEdit{
                    font-size:30px;
                    font-weight:bold;
                    border:2px solid white;
                    border-radius:8px;
                    padding:6px;
                    background:#202020;
                    color:white;
                }
            """)


            self.guess_layout.addWidget(
                edit
            )

            self.guess_boxes.append(
                edit
            )



    def clear_guess_fields(self):

        while self.guess_layout.count():

            item = self.guess_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()


        self.guess_boxes.clear()



    def get_guess(self):

        return [
            box.text().strip()
            for box in self.guess_boxes
        ]



    def show_guess_result(
            self,
            correct_words
    ):

        guesses = self.get_guess()


        for i, box in enumerate(self.guess_boxes):

            if i >= len(correct_words):
                break


            if normalize_word(
                guesses[i]
            ) == normalize_word(
                correct_words[i]
            ):


                box.setStyleSheet("""
                    QLineEdit{
                        background:#2E7D32;
                        color:white;
                        font-size:30px;
                        font-weight:bold;
                        border:2px solid white;
                        border-radius:8px;
                    }
                """)


            else:

                box.setStyleSheet("""
                    QLineEdit{
                        background:#C62828;
                        color:white;
                        font-size:30px;
                        font-weight:bold;
                        border:2px solid white;
                        border-radius:8px;
                    }
                """)


                box.setText(
                    correct_words[i]
                )



    def show_full_lyrics(
            self,
            lyrics
    ):

        self.header.setText(
            "POPRAWNY TEKST"
        )

        self.current_label.setText(
            lyrics
        )

        self.next_label.clear()

        self.clear_guess_fields()



    def clear(self):

        self.header.setText(
            "TAK TO LECIAŁO"
        )

        self.current_label.clear()

        self.next_label.clear()

        self.clear_guess_fields()