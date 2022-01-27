import datetime

class Protocol:
    def __init__(self, id, date: datetime.datetime, rating, notes, appeal = False):
        self.id = id
        self.date = date
        self.rating = rating
        self.notes = notes
        self.appeal = appeal