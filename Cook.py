from PIL import Image

class Cook:
    def __init__(self):
        self.cola_image = Image.open("Cola.png").convert("RGBA")
        self.cola_prepared = False

    def prepare_cola(self):
        self.cola_prepared = True

    def display_cola(self, background):
        if self.cola_prepared:
            background.paste(self.cola_image, (50, 50), self.cola_image)
        return background
