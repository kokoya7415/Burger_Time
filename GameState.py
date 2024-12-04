class GameState:
    def __init__(self, maxVisit=7):
        self.ticks = 0
        self.score = 0
        self.visited = 0
        self.waitCount = 15
        self.maxVisit = maxVisit
        self.running = True  # 게임 실행 상태 제어를 위한 속성

    def update_ticks(self):
        """Increment the game ticks."""
        self.ticks += 1

    def update_score(self, visitor):
        """Update the score based on visitor's purchase status."""
        if visitor.buy:
            self.score += 1

    def is_game_over(self):
        """Check if the game is over."""
        return self.visited >= self.maxVisit

    def decrement_wait_time(self, visitor):
        """Decrement visitor's wait time."""
        if self.ticks % 15 == 0 and visitor.state == 1:
            visitor.wait_time -= 1
