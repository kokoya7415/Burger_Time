# JoyStick.py

from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789
import board
from digitalio import DigitalInOut, Direction
import time

class Joystick:
    def __init__(self):
        # 디스플레이 설정
        cs_pin = DigitalInOut(board.CE0)
        dc_pin = DigitalInOut(board.D25)
        reset_pin = DigitalInOut(board.D24)
        BAUDRATE = 24000000

        spi = board.SPI()
        self.disp = st7789.ST7789(
            spi,
            height=240,
            y_offset=80,
            rotation=180,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=BAUDRATE,
        )

        # 백라이트 설정
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output(value=True)  # 백라이트를 항상 켜둠

        # 버튼 설정
        self.buttons = {
            "A": DigitalInOut(board.D5),
            "L": DigitalInOut(board.D27),
            "R": DigitalInOut(board.D23),
            "U": DigitalInOut(board.D17),
            "D": DigitalInOut(board.D22)
        }
        for button in self.buttons.values():
            button.direction = Direction.INPUT

        # 초기 위치와 디스플레이 크기 설정
        self.width, self.height = self.disp.width, self.disp.height
        self.current_position = 0

        # 아이템 위치 좌표 설정
        self.item_positions = [
            (0, 149, 32, 170),   # 아래빵
            (31, 148, 69, 170),  # 패티
            (69, 148, 100, 170), # 치즈
            (0, 172, 33, 195),   # 토마토
            (32, 172, 69, 195),  # 양상추
            (69, 172, 100, 195), # 위에빵
            (106, 142, 155, 198),# 후라이팬
            (160, 150, 195, 193),# 튀김기
            (198, 147, 232, 193),# 감자 모음
            (0, 100, 47, 137),    # 계산대
            (185, 0, 238, 95)    # 콜라 냉장고
        ]

    def display_image(self, image_path):
        image = Image.open(image_path).resize((self.width, self.height))
        self.disp.image(image)

    def draw_selection_box(self):
        image = Image.open("Fund.jpg").resize((self.width, self.height)).convert("RGB")
        draw = ImageDraw.Draw(image)
        x1, y1, x2, y2 = self.item_positions[self.current_position]
        draw.rectangle((x1, y1, x2, y2), outline="red", width=3)
        self.disp.image(image)

    def update_position(self):
        # 조이스틱 이동 논리 구현
        if self.current_position in [0, 1, 2, 6, 7, 8] and not self.buttons["U"].value:
            self.current_position = 9
        elif self.current_position == 9 and not self.buttons["D"].value:
            self.current_position = 0
        elif self.current_position == 9 and not self.buttons["U"].value:
            self.current_position = 10
        elif self.current_position == 10 and not self.buttons["D"].value:
            self.current_position = 9
        elif self.current_position == 10 and not self.buttons["U"].value:
            return
        elif self.current_position == 9 and not self.buttons["L"].value:
            return
        elif self.current_position == 3 and not self.buttons["L"].value:
            return
        elif self.current_position in [3, 4, 5, 6, 7, 8] and not self.buttons["D"].value:
            return
        elif self.current_position == 8 and not self.buttons["R"].value:
            return
        elif not self.buttons["U"].value:
            self.current_position = max(0, self.current_position - 3)
        elif not self.buttons["D"].value:
            self.current_position = min(len(self.item_positions) - 1, self.current_position + 3)
        elif not self.buttons["L"].value:
            if self.current_position == 6:
                self.current_position = 2
            else:
                self.current_position = max(0, self.current_position - 1)
        elif not self.buttons["R"].value:
            if self.current_position == 2:
                self.current_position = 6
            else:
                self.current_position = min(len(self.item_positions) - 1, self.current_position + 1)