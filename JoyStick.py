from PIL import Image, ImageDraw
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_rgb_display import st7789

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
        self.backlight.switch_to_output(value=True)

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
            (0, 149, 32, 195),   # 빵
            (31, 148, 69, 195),  # 양상추
            (69, 148, 100, 195), # 소세지
            (167, 141, 195, 192),# 머스타드
            (198, 141, 228, 192),# 케챱
            (0, 100, 47, 137),    # 계산대
            (185, 0, 238, 95)    # 콜라 냉장고
        ]

    def display_image(self, image_path):
        image = Image.open(image_path).resize((self.width, self.height))
        self.disp.image(image)

    def draw_selection_box(self, background):
        # 현재 선택된 위치에 빨간색 테두리를 그림
        x1, y1, x2, y2 = self.item_positions[self.current_position]
        draw = ImageDraw.Draw(background)
        draw.rectangle((x1, y1, x2, y2), outline="red", width=3)
        return background

    def update_position(self):
        # 각 위치에서의 이동 방향을 설정
        position_map = {
            0: {"U": 5, "R": 1},   # 빵
            1: {"L": 0, "U": 5, "R": 2},   # 양상추
            2: {"L": 1, "U": 5, "R": 3},   # 소세지
            3: {"L": 2, "U": 5, "R": 4},   # 머스타드
            4: {"L": 3, "U": 5},   # 케챱
            5: {"D": 0, "U": 6, "R": 6},   # 계산대
            6: {"D": 5, "L": 5}    # 콜라냉장고
        }

        # 방향에 따라 이동
        if not self.buttons["U"].value and "U" in position_map[self.current_position]:
            self.current_position = position_map[self.current_position]["U"]
        elif not self.buttons["D"].value and "D" in position_map[self.current_position]:
            self.current_position = position_map[self.current_position]["D"]
        elif not self.buttons["L"].value and "L" in position_map[self.current_position]:
            self.current_position = position_map[self.current_position]["L"]
        elif not self.buttons["R"].value and "R" in position_map[self.current_position]:
            self.current_position = position_map[self.current_position]["R"]