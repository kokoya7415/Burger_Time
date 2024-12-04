from gpiozero import Button  # type: ignore

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

def setup_button(pin):
    button = Button(pin)
    return button
