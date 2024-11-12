from PIL import Image, ImageDraw, ImageFont
import random
import time

class Visitor:
    def __init__(self, joystick, background, point_heart, cook):
        self.joystick = joystick
        self.visitor_images = [Image.open("Girl.png").convert("RGBA"), Image.open("Boy.png").convert("RGBA")]
        self.visitor_image = random.choice(self.visitor_images)
        self.visitor_position = -self.visitor_image.width
        self.stopped = False
        self.initial_background = background.copy()
        self.point_heart = point_heart
        self.cook = cook
        self.speech_bubble = Image.open("Say.png").convert("RGBA")

    def move_and_display_visitor(self):
        while self.visitor_position < 10:
            if not self.stopped:
                self.visitor_position += 5
                background = self.initial_background.copy()
                background.paste(self.visitor_image, (int(self.visitor_position), 0), self.visitor_image)
                background = self.point_heart.display_heart(background)
                background = self.draw_selection_box(background)
                self.joystick.disp.image(background)
                time.sleep(0.1)
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
        background = self.initial_background.copy()
        background.paste(self.visitor_image, (int(self.visitor_position), 0), self.visitor_image)
        # 말풍선을 약간 오른쪽으로 이동 (5픽셀)
        background.paste(self.speech_bubble, (int(self.visitor_position) - 30, 10), self.speech_bubble)
        background = self.point_heart.display_heart(background)
        background = self.draw_selection_box(background)
        self.joystick.disp.image(background)

    def start_countdown(self):
        countdown_time = 15
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)

        for i in range(countdown_time, -1, -1):
            start_time = time.time()
            while time.time() - start_time < 1:
                background = self.initial_background.copy()
                background.paste(self.visitor_image, (int(self.visitor_position), 0), self.visitor_image)
                # 말풍선을 약간 오른쪽으로 이동 (5픽셀)
                background.paste(self.speech_bubble, (int(self.visitor_position) - 30, 10), self.speech_bubble)
                background = self.point_heart.display_heart(background)
                background = self.draw_selection_box(background)

                # 카운트다운 텍스트 표시
                draw = ImageDraw.Draw(background)
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
        while self.visitor_position > -self.visitor_image.width:
            self.visitor_position -= 5
            background = self.initial_background.copy()
            background.paste(self.visitor_image, (int(self.visitor_position), 0), self.visitor_image)
            background = self.point_heart.display_heart(background)
            background = self.draw_selection_box(background)
            self.joystick.disp.image(background)
            self.joystick.update_position()
            time.sleep(0.05)

    def draw_selection_box(self, background):
        draw = ImageDraw.Draw(background)
        x1, y1, x2, y2 = self.joystick.item_positions[self.joystick.current_position]
        draw.rectangle((x1, y1, x2, y2), outline="red", width=3)
        return background
