import random
from PIL import Image, ImageDraw, ImageFont
import board
from gpiozero import Button # type: ignore
from digitalio import DigitalInOut
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import time

spi = board.SPI()
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
def setup_button(pin):
    button = Button(pin)
    return button


# 백라이트와 버튼 설정
backlight = DigitalInOut(board.D26)
backlight.switch_to_output(value=True)
buttons = {name: setup_button(pin) for name, pin in [
    ("A", 5), ("L", 27), ("R", 23)
]}



class Visitor:
    def __init__(self,wait_cnt):
        is_girl = random.randint(0, 1)
        if is_girl:
            self.img = Image.open("Girl.png").convert("RGBA")
        else:
            self.img = Image.open("Boy.png").convert("RGBA")
        self.pos = -self.img.width

        self.state = 0  # 0: coming, 1: waiting, 2: leaving, 3: done
        self.wait_time = wait_cnt

        order = [0,1,2,3] if random.randint(0,1) else [0,1,2,4]
        self.order = [order, random.randint(0,1)] # 앞부분은 오더 순서, 뒷부분은 콜라 유무

        self.buy = False

    def move(self):
        if self.state == 0:
            self.pos += 5
            if self.pos >= 10:
                self.state = 1
                self.pos = 10

        elif self.state == 1:
            if self.wait_time == 0:
                self.state = 2

        elif self.state == 2:
            self.pos -= 5
            if self.pos <= -self.img.width//2:
                self.state = 3
        else:
            pass


class Joystick:
    def __init__(self):
        self.item_positions = [
            (5, 155), (35, 155), (75, 155),
            (170, 150), (205, 150), (5, 105), (190, 0)
        ]

        self.current_position = 0

    def goLeft(self):
        self.current_position = max(0, self.current_position - 1)

    def goRight(self):
        self.current_position = min(len(self.item_positions) - 1, self.current_position + 1)


class Cook:
    def __init__(self, order):
        self.step = 0
        self.order = order
        self.isDone = False
        self.sell_able = False
        self.cola_Done = not self.order[1]
        self.img = Image.new("RGBA",(240,240),(0,0,0,0))
        

    def nextStep(self, act):
        if self.isDone and act==5:
            print("Sell!")
            self.sell_able = True
        else:
            if len(self.order[0]) > self.step and self.order[0][self.step] == act:
                self.img.paste(hotdogImages[self.order[0][self.step]],(0,0),hotdogImages[self.order[0][self.step]])
                self.step += 1
                print("Correct")
                
            else:
                print("Wrong")
                
            if self.order[1] and act==6:
                self.cola_Done = True

            if self.step == len(self.order[0]) and self.cola_Done:
                print("Order Done")
                self.isDone = True
        
        print(self.step,self.order, self.cola_Done)


bgImage = Image.open("Fund.png").resize((240, 240)).convert("RGB")
bubbleImage = Image.open("Say.png").convert("RGBA")
colaImage = Image.open("Cola.png").convert("RGBA")

breadImage = Image.open("Bread.png").convert("RGBA")
vegetableImage = Image.open("Vegetable.png").convert("RGBA")
meatImage = Image.open("Meat.png").convert("RGBA")

mustardImage = Image.open("Mustard.png").convert("RGBA")
ketchupImage = Image.open("Ketchup.png").convert("RGBA")

handImage = Image.open("Hand.png").convert("RGBA").resize((30,30))
hotdogImage = [
    Image.open("Mustard_Dog.png").convert("RGBA").resize((160,160)),
    Image.open("ketchup_Dog.png").convert("RGBA").resize((160,160))
]


hotdogImages = [
    breadImage,
    vegetableImage,
    meatImage,
    mustardImage,
    ketchupImage
]

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)  # 적절히 크기 조정된 폰트
joy = Joystick()
visitor = Visitor(wait_cnt=15)
cook = Cook(visitor.order)


buttons['L'].when_pressed = joy.goLeft
buttons['R'].when_pressed = joy.goRight

def keyA_():
    global start
    start = True
buttons['A'].when_pressed = keyA_

ticks = 0

homeImage = [Image.open("Start.png"),Image.open("Start_.png")]
start = False
flag = 0
while not start:
    # display
    disp.image(homeImage[0])
    time.sleep(0.1)
    
    flag = 1 - flag
             
def keyA():
    global visitor, cook, joy

    if visitor.state == 1:
        cook.nextStep(joy.current_position)
buttons['A'].when_pressed = keyA   

maxVisit = 7
visited = 0
score = 0
waitCount = 15
bg = bgImage.copy()
running = True
while running:

    # update
    visitor.move()
    if ticks % 15 == 0 and visitor.state == 1:
        visitor.wait_time -= 1
    if visitor.state == 3:
        score += visitor.buy 
        if not visitor.buy:
            break
        waitCount-= random.randint(1,2)
        visitor = Visitor(waitCount)
        cook = Cook(visitor.order)
        visited+=1
        
        if visited == maxVisit:
            break
        
    if cook.sell_able:
        visitor.buy = 1
        visitor.state = 2

    # draw
    bg = bgImage.copy()
    bg.paste(visitor.img, (int(visitor.pos), 0), visitor.img)
    if visitor.state == 1:
        bg.paste(bubbleImage, (-20, 10), bubbleImage)
        bg.paste(
            hotdogImage[cook.order[0][3]-3],
            (40,0),
            hotdogImage[cook.order[0][3]-3],
        )
        if cook.order[1]:
            bg.paste(
                colaImage,
                (25,-70),
                colaImage
            )
        
    
    if cook.order[1] and cook.cola_Done and not visitor.buy:
        bg.paste(colaImage, (0,10),colaImage)    # 콜라 위취
        
    draw = ImageDraw.Draw(bg)
    handPos = joy.item_positions[joy.current_position]
    bg.paste(handImage,handPos,handImage)
    if visitor.state == 1:
        text_bbox = draw.textbbox((0, 0), str(visitor.wait_time), font=font)
        text_x = (240 - (text_bbox[2] - text_bbox[0])) // 2
        text_y = 240 - (text_bbox[3] - text_bbox[1]) - 12  # 살짝 더 올리기 위해 -9에서 -12로 수정
        # Draw text with slight bold effect
        draw.text((text_x, text_y), str(visitor.wait_time), font=font, fill="white")
        draw.text((text_x + 1, text_y), str(visitor.wait_time), font=font, fill="white")
        
    # Draw text with slight bold effect Score
    draw.text((10,210), str(score), font=font, fill="black")
    draw.text((11,210), str(score), font=font, fill="black")
    
    
    if not visitor.buy:
        bg.paste(cook.img,(0,0),cook.img)
    
    if visitor.buy:
        bg.paste(
            hotdogImage[cook.order[0][3]-3],
            (visitor.pos-40,-30),
            hotdogImage[cook.order[0][3]-3],
        )
        if cook.order[1]:
            bg.paste(
                colaImage,
                (25+visitor.pos-70,-20),
                colaImage
            )

    # display
    disp.image(bg)
    time.sleep(0.01)
    ticks += 1

isGoodEnding = score == 7
endingImage = [
    Image.open("Bad_Ending.jpg"),
    Image.open("Good_Ending.jpg")
]
endingImage = endingImage[isGoodEnding]
disp.image(endingImage)