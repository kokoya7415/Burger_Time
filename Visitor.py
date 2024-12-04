import random
from PIL import Image

class Visitor:
    def __init__(self, wait_cnt):
        is_girl = random.randint(0, 1)
        if is_girl:
            self.img = Image.open("Girl.png").convert("RGBA")
        else:
            self.img = Image.open("Boy.png").convert("RGBA")
        self.pos = -self.img.width

        self.state = 0  # 0: coming, 1: waiting, 2: leaving, 3: done
        self.wait_time = wait_cnt

        order = [0, 1, 2, 3] if random.randint(0, 1) else [0, 1, 2, 4]
        self.order = [order, random.randint(0, 1)]  # 앞부분은 오더 순서, 뒷부분은 콜라 유무

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
            if self.pos <= -self.img.width // 2:
                self.state = 3
        else:
            pass

            