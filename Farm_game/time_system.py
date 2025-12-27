class TimeSystem:
    def __init__(self):
        self.time = 6.0
        self.day = 1

    def update(self):
        self.time += 0.01
        if self.time >= 24:
            self.time = 0
            self.day += 1
