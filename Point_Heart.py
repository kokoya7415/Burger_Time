from PIL import Image

class PointHeart:
    def __init__(self, joystick):
        self.joystick = joystick
        self.heart_image = Image.open("Heart_1.png")

    def display_heart(self, background):
        background.paste(self.heart_image, (0, 0), self.heart_image)
        return background

    def decrease_heart(self):
        updated_background = Image.open("Fund.png").resize((self.joystick.width, self.joystick.height)).convert("RGB")
        self.joystick.disp.image(updated_background)
        self.show_sad_ending()

    def show_sad_ending(self):
        sad_ending = Image.open("Ending.png").resize((self.joystick.width, self.joystick.height))
        self.joystick.disp.image(sad_ending)
