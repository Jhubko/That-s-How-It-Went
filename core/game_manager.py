class GameManager:

    def __init__(self):

        self.song = None
        self.songs = []
        self.category = None

        self.music_playing = False

        self.full_lyrics = []
        self.hidden_lyrics = []

        self.stop_time = 0
        self.selected_line_index = None
        self.selected_line = None
        self.stop_used = False
        self.song_used = False

game = GameManager()