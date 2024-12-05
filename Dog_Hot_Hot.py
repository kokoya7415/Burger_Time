import random
import time
from PIL import Image, ImageDraw, ImageFont
from Display import setup_display, setup_backlight
from GameState import GameState
from Visitor import Visitor
from Joystick import Joystick, setup_button
from Cook import Cook
from Image import (
    bgImage,
    bubbleImage,
    colaImage,
    handImage,
    hotdogImage,
    hotdogImages,
)

# 디스플레이 및 백라이트 설정
disp = setup_display()
backlight = setup_backlight()

# 버튼 설정
buttons = {name: setup_button(pin) for name, pin in [("A", 5), ("L", 27), ("R", 23)]}

# 게임 초기화
state = GameState(maxVisit=7)
joy = Joystick()
visitor = Visitor(wait_cnt=state.waitCount)
cook = Cook(visitor.order)

# 버튼 핸들러 설정
buttons['L'].when_pressed = joy.goLeft
buttons['R'].when_pressed = joy.goRight

def keyA():
    global visitor, cook, joy, state, start
    start = True
    if visitor.state == 1:
        cook.nextStep(joy.current_position)

buttons['A'].when_pressed = keyA

# 폰트 및 시작 화면
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
homeImage = [Image.open("Start.png"), Image.open("Start_.png")]
start = False
flag = 0

# 시작 화면 루프
while not start:
    disp.image(homeImage[flag].convert("RGB"))
    time.sleep(0.1)
    flag = 1 - flag

# 메인 게임 루프
bg = bgImage.copy()
while state.running:
    # 상태 업데이트
    state.update_ticks()
    visitor.move()
    state.decrement_wait_time(visitor)

    if visitor.state == 3:  # Visitor has left
        state.update_score(visitor)
        if not visitor.buy:
            state.running = False  # 게임 종료
            break
        state.waitCount -= random.randint(1, 2)
        visitor = Visitor(state.waitCount)
        cook = Cook(visitor.order)
        state.visited += 1

        if state.is_game_over():
            state.running = False  # 게임 종료
            break

    if cook.sell_able:
        visitor.buy = 1
        visitor.state = 2

    # 화면 그리기
    bg = bgImage.copy()
    bg.paste(visitor.img, (int(visitor.pos), 0), visitor.img)
    if visitor.state == 1:
        bg.paste(bubbleImage, (-20, 10), bubbleImage)
        bg.paste(hotdogImage[cook.order[0][3] - 3], (40, 0), hotdogImage[cook.order[0][3] - 3])
        if cook.order[1]:
            bg.paste(colaImage, (25, -70), colaImage)

    if cook.order[1] and cook.cola_Done and not visitor.buy:
        bg.paste(colaImage, (0, 10), colaImage)

    draw = ImageDraw.Draw(bg)
    handPos = joy.item_positions[joy.current_position]
    bg.paste(handImage, handPos, handImage)

    if visitor.state == 1:
        text_bbox = draw.textbbox((0, 0), str(visitor.wait_time), font=font)
        text_x = (240 - (text_bbox[2] - text_bbox[0])) // 2
        text_y = 240 - (text_bbox[3] - text_bbox[1]) - 12
        draw.text((text_x, text_y), str(visitor.wait_time), font=font, fill="white")
        draw.text((text_x + 1, text_y), str(visitor.wait_time), font=font, fill="white")

    draw.text((10, 210), str(state.score), font=font, fill="black")
    draw.text((11, 210), str(state.score), font=font, fill="black")

    if not visitor.buy:
        bg.paste(cook.img, (0, 0), cook.img)

    if visitor.buy:
        bg.paste(hotdogImage[cook.order[0][3] - 3], (visitor.pos - 40, -30), hotdogImage[cook.order[0][3] - 3])
        if cook.order[1]:
            bg.paste(colaImage, (25 + visitor.pos - 70, -20), colaImage)

    disp.image(bg.convert("RGB"))
    time.sleep(0.01)

# 엔딩 화면
isGoodEnding = state.score == 7
endingImage = [
    Image.open("Bad_Ending.jpg"),
    Image.open("Good_Ending.jpg")
]
disp.image(endingImage[isGoodEnding].convert("RGB"))
