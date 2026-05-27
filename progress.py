class Progress:
    def __init__(self):
        self.connection_points = 0
        self.phone_answered = False
        self.ticket_found = False
        self.conductor_task_started = False

    def add_connection_point(self):
        self.connection_points += 1

    def mark_phone_answered(self):
        self.phone_answered = True

    def start_conductor_task(self):
        self.conductor_task_started = True

    def mark_ticket_found(self):
        self.ticket_found = True