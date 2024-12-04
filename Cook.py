from PIL import Image
from Image import hotdogImages  # hotdogImages를 Image 모듈에서 가져옴


class Cook:
    def __init__(self, order):
        self.step = 0
        self.order = order
        self.isDone = False
        self.sell_able = False
        self.cola_Done = not self.order[1]
        self.img = Image.new("RGBA", (240, 240), (0, 0, 0, 0))

    def nextStep(self, act):
        if self.isDone and act == 5:
            print("Sell!")
            self.sell_able = True
        else:
            if len(self.order[0]) > self.step and self.order[0][self.step] == act:
                self.img.paste(
                    hotdogImages[self.order[0][self.step]],
                    (0, 0),
                    hotdogImages[self.order[0][self.step]]
                )
                self.step += 1
                print("Correct")
            else:
                print("Wrong")

            if self.order[1] and act == 6:
                self.cola_Done = True

            if self.step == len(self.order[0]) and self.cola_Done:
                print("Order Done")
                self.isDone = True

        print(self.step, self.order, self.cola_Done)
