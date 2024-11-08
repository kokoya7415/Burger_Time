import time
from PIL import Image
from JoyStick import Joystick
from Visitor import Visitor
from Point_Heart import PointHeart
from Cook import Cook  # Cook 클래스를 불러옴

# Joystick 인스턴스 생성
joystick = Joystick()
joystick.backlight.value = True  # 백라이트를 켜둠 (항상 유지)

# Start.png 이미지를 먼저 표시
joystick.display_image("Start.png")

# 버튼 #5 (button_A)가 눌릴 때까지 대기
while True:
    if not joystick.buttons["A"].value:
        # Fund.jpg를 배경으로 불러오기
        background = Image.open("Fund.jpg").resize((joystick.width, joystick.height)).convert("RGB")
        
        # 하트와 콜라 준비 인스턴스 생성
        point_heart = PointHeart(joystick)
        cook = Cook(joystick)  # Cook 인스턴스 생성
        
        # 하트를 Fund 이미지와 함께 표시
        background = point_heart.display_heart(background)
        joystick.disp.image(background)
        break
    time.sleep(0.1)

# Visitor 생성 및 8번 등장 반복
for _ in range(8):
    visitor = Visitor(joystick, background, point_heart)
    visitor.move_and_display_visitor()

# 조이스틱 탐색 가능 (엔딩 전까지 무한 루프)
while True:
    background = Image.open("Fund.jpg").resize((joystick.width, joystick.height)).convert("RGB")
    
    # 콜라가 조리되었을 때 배경에 표시되도록 설정
    background = point_heart.display_heart(background)
    background = cook.cook_cola(background)  # 콜라 조리 상태 업데이트
    
    joystick.update_position()
    joystick.draw_selection_box()
    joystick.disp.image(background)  # 항상 하트와 콜라가 보이도록 배경 업데이트
    time.sleep(0.1)
# asdf