

class Application:

    def __init__(
            self,
            height: int,
            width: int,
    ):
        self.height = height
        self.width = width

    def get_title(self) -> str:
        pass

    def init_graphics(self):
        pass

    def display(self):
        pass

    def update(self):
        pass

    def key_pressed(self, key: int):
        pass

    def mouse_pressed(self, button: int, state: int, x: int, y: int):
        pass


