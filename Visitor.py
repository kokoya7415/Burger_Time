from PIL import Image, ImageDraw, ImageFont
import random
import time
from Cook import Cook

class Visitor:
    def __init__(self, joystick, background, point_heart):
        self.joystick = joystick
        self.visitor_images = [Image.open("Girl.png").convert("RGBA"), Image.open("Boy.png").convert("RGBA")]
        self.visitor_image = random.choice(self.visitor_images)
        self.visitor_position = -self.visitor_image.width + 100
        self.stopped = False
        self.background = background.copy()  # 초기 배경 이미지
        self.point_heart = point_heart
        self.cook = Cook(joystick)  # Cook 인스턴스 생성

        # 말풍선 이미지 로드
        self.speech_bubble = Image.open("Say.png").convert("RGBA")  # 말풍선 이미지도 RGBA로 변환

    def move_and_display_visitor(self):
        while self.visitor_position < 10:
            if not self.stopped:
                self.visitor_position += 5
                background = self.background.copy().convert("RGB")
                
                # 방문객 위치에 맞게 그림 추가
                background.paste(self.visitor_image, (self.visitor_position, 0), self.visitor_image)
                background = self.point_heart.display_heart(background)  # 하트를 포함한 배경 업데이트
                
                # 빨간 네모 그리기
                draw = ImageDraw.Draw(background)
                x1, y1, x2, y2 = self.joystick.item_positions[self.joystick.current_position]
                draw.rectangle((x1, y1, x2, y2), outline="red", width=3)
                
                self.joystick.disp.image(background)
                time.sleep(0.1)
                
                # 조이스틱 입력 처리
                self.joystick.update_position()
            else:
                self.show_speech_bubble()
                self.start_countdown()
                break

        if not self.stopped:
            self.stopped = True
            self.show_speech_bubble()
            self.start_countdown()

    def show_speech_bubble(self):
        background = self.background.copy().convert("RGB")
        
        background.paste(self.visitor_image, (self.visitor_position, 0), self.visitor_image)
        background.paste(self.speech_bubble, (self.visitor_position - 40, 10), self.speech_bubble)
        background = self.point_heart.display_heart(background)  # 하트를 포함한 배경 업데이트
        
        draw = ImageDraw.Draw(background)
        x1, y1, x2, y2 = self.joystick.item_positions[self.joystick.current_position]
        draw.rectangle((x1, y1, x2, y2), outline="red", width=3)
        
        self.joystick.disp.image(background)

    def start_countdown(self):
        countdown_time = 15
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)

        for i in range(countdown_time, -1, -1):
            start_time = time.time()
            while time.time() - start_time < 1:
                background = self.background.copy().convert("RGB")
                background.paste(self.visitor_image, (self.visitor_position, 0), self.visitor_image)
                background.paste(self.speech_bubble, (self.visitor_position - 40, 10), self.speech_bubble)
                
                # 콜라가 조리될 수 있는 상태로 Cook 클래스 호출
                background = self.cook.cook_cola(background)  # 콜라 조리 상태 업데이트
                background = self.point_heart.display_heart(background)  # 하트를 포함한 배경 업데이트
                
                # 빨간 네모 그리기
                draw = ImageDraw.Draw(background)
                x1, y1, x2, y2 = self.joystick.item_positions[self.joystick.current_position]
                draw.rectangle((x1, y1, x2, y2), outline="red", width=3)
                
                # 카운트다운 텍스트 표시
                text = f"{i}"
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_x = (self.joystick.width - (text_bbox[2] - text_bbox[0])) // 2
                text_y = self.joystick.height - (text_bbox[3] - text_bbox[1]) - 9
                draw.text((text_x, text_y), text, font=font, fill="white")
                
                self.joystick.disp.image(background)
                self.joystick.update_position()
                time.sleep(0.05)

        time.sleep(2)
        self.clear_visitor()

    def clear_visitor(self):
        for _ in range(20):
            self.visitor_position -= 5
            background = self.background.copy().convert("RGB")
            background.paste(self.visitor_image, (self.visitor_position, 0), self.visitor_image)
            background = self.point_heart.display_heart(background)
            
            draw = ImageDraw.Draw(background)
            x1, y1, x2, y2 = self.joystick.item_positions[self.joystick.current_position]
            draw.rectangle((x1, y1, x2, y2), outline="red", width=3)
            
            self.joystick.disp.image(background)
            self.joystick.update_position()
            time.sleep(0.05)
