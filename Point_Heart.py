# Point_Heart.py

from PIL import Image

class PointHeart:
    def __init__(self, joystick):
        self.joystick = joystick
        self.heart_image = Image.open("Heart_1.png")

    def display_heart(self, background):
        # Heart_1을 원래 이미지 위치와 크기로 출력
        background.paste(self.heart_image, (0, 0), self.heart_image)  # 위치 조정 없이 원본 그대로 표시
        return background

    def decrease_heart(self):
        # Heart_1을 화면에서 지우는 방식으로 목숨 감소
        updated_background = Image.open("Fund.png").resize((self.joystick.width, self.joystick.height)).convert("RGB")
        self.joystick.disp.image(updated_background)

        # 목숨이 없어지면 새드엔딩을 표시
        self.show_sad_ending()

    def show_sad_ending(self):
        sad_ending = Image.open("Ending.png").resize((self.joystick.width, self.joystick.height))
        self.joystick.disp.image(sad_ending)