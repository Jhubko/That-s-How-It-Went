from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QFrame,
    QScrollArea
)

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QProgressBar
from utils.text_utils import normalize_word


class PlayerScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "TAK TO LECIAŁO - PLAYER.EXE"
        )

        self.resize(
            1200,
            700
        )

        self.setStyleSheet("""
            QWidget {
                background-color: #008080;
            }
        """)

        main_layout = QVBoxLayout()

        self.panel = QFrame()

        self.panel.setStyleSheet("""
            QFrame {
                background-color: #c0c0c0;
                border: 3px solid;
                border-top-color: white;
                border-left-color: white;
                border-right-color: #404040;
                border-bottom-color: #404040;
            }
        """)

        main_layout.addWidget(
            self.panel
        )

        layout = QVBoxLayout(
            self.panel
        )

        self.blink_state = False

        self.blink_timer = QTimer()

        self.blink_timer.timeout.connect(
            self.blink_text
        )


        self.header = QLabel(
            "TAK TO LECIAŁO!"
        )

        self.header.setAlignment(
            Qt.AlignCenter
        )

        self.header.setStyleSheet("""
            QLabel {
                font-family: Tahoma;
                font-size:32px;
                font-weight:bold;
                color:white;
                background:#000080;
                padding:8px;
                border:3px outset white;
            }
        """)

        layout.addWidget(
            self.header
        )

        self.current_label = QLabel()

        self.current_label.setAlignment(
            Qt.AlignCenter
        )

        self.current_label.setWordWrap(
            True
        )

        self.current_label.setStyleSheet("""
            QLabel {
                font-family: Verdana;
                font-size:36px;
                font-weight:bold;
                color:black;
                background:white;
                border:4px solid gray;
                padding:20px;
            }
        """)

        self.scroll_area = QScrollArea()

        self.scroll_area.setMinimumHeight(
            200
        )

        self.scroll_area.setMaximumHeight(
            350
        )

        self.scroll_area.setWidgetResizable(
            True
        )

        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background:white;
                border:0px;
            }

            QScrollBar:vertical {
                width:20px;
            }
        """)

        self.scroll_area.setWidget(
            self.current_label
        )

        layout.addWidget(
            self.scroll_area
        )

        self.next_label = QLabel()

        self.next_label.setAlignment(
            Qt.AlignCenter
        )

        self.next_label.setWordWrap(
            True
        )

        self.next_label.setStyleSheet("""
            QLabel {
                font-family: Verdana;
                font-size:28px;
                color:#555555;
                background:#EEEEEE;
                border:3px inset gray;
                padding:10px;
            }
        """)

        layout.addWidget(
            self.next_label
        )


        self.guess_layout = QHBoxLayout()

        self.guess_layout.setAlignment(
            Qt.AlignCenter
        )

        layout.addLayout(
            self.guess_layout
        )


        self.guess_boxes = []

        self.loading_label = QLabel(
            "ŁADOWANIE..."
        )

        self.loading_label.setAlignment(
            Qt.AlignCenter
        )

        self.loading_label.setStyleSheet("""
            QLabel {
                font-family: Tahoma;
                font-size:24px;
                font-weight:bold;
                background:#c0c0c0;
                border:3px inset gray;
                padding:10px;
            }
        """)

        self.loading_bar = QProgressBar()

        self.loading_bar.setRange(
            0,
            100
        )

        self.loading_bar.setValue(
            0
        )

        self.loading_bar.setTextVisible(
            False
        )

        self.loading_bar.setFixedHeight(
            30
        )

        self.loading_bar.setStyleSheet("""
            QProgressBar {
                background:#808080;
                border:3px inset white;
            }

            QProgressBar::chunk {
                background:#000080;
            }
        """)

        self.loading_label.hide()
        self.loading_bar.hide()

        layout.addWidget(
            self.loading_label
        )

        layout.addWidget(
            self.loading_bar
        )

        self.setLayout(
            main_layout
        )


    def show_categories(self, categories):

        self.stop_blink()

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

        self.stop_blink()

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

        self.stop_blink()

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
            "★ ŚPIEWAJ! ★"
        )

        self.blink_timer.start(
            500
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

        self.stop_blink()

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
                metrics.horizontalAdvance(clean_word)
                + 50
            )

            edit.setFixedWidth(
                max(width,120)
            )

            edit.setFixedHeight(
                60
            )

            edit.setStyleSheet("""
                QLineEdit {
                    font-family: Courier New;
                    font-size:28px;
                    font-weight:bold;
                    border:3px outset white;
                    background:#FFFFCC;
                    color:black;
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
                    QLineEdit {
                        background:#00AA00;
                        color:white;
                        font-size:30px;
                        font-weight:bold;
                    }
                """)

            else:

                box.setStyleSheet("""
                    QLineEdit {
                        background:#AA0000;
                        color:white;
                        font-size:30px;
                        font-weight:bold;
                    }
                """)

                box.setText(
                    correct_words[i]
                )



    def show_full_lyrics(
            self,
            lyrics
    ):

        self.stop_blink()

        self.header.setText(
            "POPRAWNY TEKST"
        )

        self.current_label.setText(
            lyrics
        )

        self.next_label.clear()

        self.clear_guess_fields()



    def stop_blink(self):

        self.blink_timer.stop()

        self.blink_state = False



    def blink_text(self):

        self.blink_state = not self.blink_state

        if self.blink_state:

            self.header.setText(
                "★ ŚPIEWAJ! ★"
            )

        else:

            self.header.setText(
                "TAK TO LECIAŁO"
            )



    def clear(self):

        self.stop_blink()

        self.header.setText(
            "TAK TO LECIAŁO!"
        )

        self.current_label.clear()

        self.next_label.clear()

        self.clear_guess_fields()

    def show_loading(self):

        self.header.setText(
            "TAK TO LECIAŁO - PLAYER.EXE"
        )

        self.current_label.setText(
            "ŁADOWANIE PIOSENEK..."
        )

        self.next_label.setText(
            "Proszę czekać..."
        )

        self.loading_label.show()
        self.loading_bar.show()

        self.loading_bar.setValue(
            0
        )

    def update_loading(self, value):

        self.loading_bar.setValue(
            value
        )

    def hide_loading(self):

        self.loading_label.hide()
        self.loading_bar.hide()