from PIL import Image

class Cook:
    def __init__(self, joystick):
        self.joystick = joystick
        # 경로를 상대 경로로 설정
        self.cola_image = Image.open("Cola.png")  # 콜라 이미지 로드
        self.cola_cooked = False  # 콜라 준비 여부 확인

    def cook_cola(self, background):
        # 콜라 자판기 위치에 있는지 확인 (좌표를 설정해야 합니다)
        cola_position_index = 10  # 예시로 콜라 자판기 위치가 10번 인덱스라고 가정
        if self.joystick.current_position == cola_position_index and not self.joystick.buttons["A"].value:
            # 콜라 이미지를 요리된 상태로 표시
            self.cola_cooked = True
            background.paste(self.cola_image, (150, 100), self.cola_image)  # 콜라 이미지 위치 조정
        return background
