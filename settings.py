class Settings:
    def __init__(self, win_size: tuple[int, int] = (1080, 720)) -> None:
        self.win_size = win_size
        self.frame_rate: int = 30
        self.font_size = 16

    def get_win_size(self) -> tuple[int, int]:
        return self.win_size
