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



        layout = QVBoxLayout()



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


        title.setStyleSheet(
            """
            font-size:48px;
            font-weight:bold;
            """
        )



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