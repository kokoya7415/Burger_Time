from PIL import Image, ImageDraw
import board
from digitalio import DigitalInOut, Direction
from adafruit_rgb_display import st7789

class Joystick:
    def __init__(self):
        # 디스플레이 설정
        spi = board.SPI()
        cs_pin = DigitalInOut(board.CE0)
        dc_pin = DigitalInOut(board.D25)
        reset_pin = DigitalInOut(board.D24)
        BAUDRATE = 24000000

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
        # 백라이트와 버튼 설정
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output(value=True)
        self.buttons = {name: self.setup_button(pin) for name, pin in [
            ("A", board.D5), ("L", board.D27), ("R", board.D23), ("U", board.D17), ("D", board.D22)
        ]}
        
        # 초기 위치와 디스플레이 크기 설정
        self.width, self.height = self.disp.width, self.disp.height
        self.current_position = 0
        self.item_positions = [
            (0, 149, 32, 195), (31, 148, 69, 195), (69, 148, 100, 195),
            (167, 141, 195, 192), (198, 141, 228, 192), (0, 100, 47, 137), (185, 0, 238, 95)
        ]

    def setup_button(self, pin):
        button = DigitalInOut(pin)
        button.direction = Direction.INPUT
        return button

    def display_image(self, image_path):
        image = Image.open(image_path).resize((self.width, self.height))
        self.disp.image(image)

    def draw_selection_box(self, background):
        x1, y1, x2, y2 = self.item_positions[self.current_position]
        draw = ImageDraw.Draw(background)
        draw.rectangle((x1, y1, x2, y2), outline="red", width=3)
        return background

    def update_position(self):
        position_map = {
            0: {"U": 5, "R": 1}, 1: {"L": 0, "U": 5, "R": 2},
            2: {"L": 1, "U": 5, "R": 3}, 3: {"L": 2, "U": 5, "R": 4},
            4: {"L": 3, "U": 5}, 5: {"D": 0, "U": 6, "R": 6}, 6: {"D": 5, "L": 5}
        }
        directions = ["U", "D", "L", "R"]
        for direction in directions:
            if not self.buttons[direction].value and direction in position_map[self.current_position]:
                self.current_position = position_map[self.current_position][direction]
                break
