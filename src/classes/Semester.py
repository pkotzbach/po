import datetime


class Semester:
    def __init__(self, id, startDate: datetime.datetime, endDate: datetime.datetime):
        self.id = id
        self.startDate = startDate
        self.endDate = endDate

    def range(self) -> str:
        start = self.startDate.strftime("%d/%m/%Y")
        end = self.endDate.strftime("%d/%m/%Y")
        return start + " - " + end