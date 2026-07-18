from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QStackedWidget
)

from screens.host_screen import HostScreen
from screens.player_screen import PlayerScreen



class MainWindow(QWidget):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "Tak To Leciało"
        )


        self.resize(
            1200,
            700
        )

        self.setStyleSheet("""
            QWidget {
                font-family: Tahoma;
                font-size: 14px;
            }

            QLabel {
                color: black;
                background: #c0c0c0;
                border: 3px inset #808080;
                padding: 8px;
            }

            QPushButton {
                background-color: #c0c0c0;
                color: black;
                border: 3px outset white;
                padding: 8px;
                font-family: Tahoma;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #dcdcdc;
            }

            QPushButton:pressed {
                border: 3px inset #808080;
            }

            QStackedWidget {
                background-color: #008080;
            }
        """)

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.stack = QStackedWidget()

        layout.addWidget(
            self.stack
        )


        self.setLayout(
            layout
        )

        self.player_screen = PlayerScreen()

        self.player_screen.show()

        self.host_screen = HostScreen(
            self
        )

        self.create_menu()




    def create_menu(self):

        menu = QWidget()


        layout = QVBoxLayout()



        title = QLabel(
            "TAK TO LECIAŁO"
        )

        title.setStyleSheet("""
            QLabel {
                font-family: Tahoma;
                font-size:48px;
                font-weight:bold;
                color:white;
                background:#000080;
                border:3px outset white;
                padding:10px;
            }
        """)

        start = QPushButton(
            "NOWA GRA"
        )


        start.clicked.connect(
            self.start_game
        )



        layout.addWidget(
            title
        )


        layout.addWidget(
            start
        )



        menu.setLayout(
            layout
        )


        self.menu = menu



        self.stack.addWidget(
            self.menu
        )


        self.stack.addWidget(
            self.host_screen
        )


        self.stack.setCurrentWidget(
            self.menu
        )


    def start_game(self):

        self.stack.setCurrentWidget(
            self.host_screen
        )


        self.player_screen.clear()