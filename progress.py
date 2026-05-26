class Progress:
    def __init__(self):
        self.connection_points = 0
        self.phone_answered = False

    def add_connection_point(self):
        self.connection_points += 1

    def mark_phone_answered(self):
        self.phone_answered = True