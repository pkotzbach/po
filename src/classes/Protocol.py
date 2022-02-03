import datetime
from main.classes.Hospitation import Hospitation


class Protocol:
    def __init__(
        self,
        id,
        hospitation: Hospitation,
        date: datetime.datetime,
        rating,
        appeal=False,
        notes=None,
    ):
        self.id = id
        self.hospitation = hospitation
        self.date = date
        self.rating = rating
        self.notes = notes
        self.appeal = appeal
