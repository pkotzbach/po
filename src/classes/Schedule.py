import datetime
from main.classes.Semester import Semester


class Schedule:
    def __init__(self, id, creationDate: datetime.datetime, semester: Semester):
        self.id = id
        self.creationDate = creationDate
        self.semester = semester