import datetime
from classes.Teacher import Teacher
from classes.Schedule import Schedule
from classes.Class import Class


class Hospitation:
    def __init__(
        self,
        id,
        teacher: Teacher,
        clas: Class,
        schedule: Schedule,
        date: datetime.date,
        commission: list[Teacher],
        protocolCreated,
    ):
        self.id = id
        self.teacher = teacher
        self.clas = clas
        self.schedule = schedule
        self.date = date
        self.commission = commission
        self.protocolCreated = protocolCreated

    def __str__(self) -> str:
        return (
            str(self.id)
            + ", "
            + str(self.teacher.id)
            + ", "
            + str(self.schedule.id)
            + ", "
            + str(self.clas.id)
            + ", "
            + str(self.date)
            + ", "
            + str(len(self.commission))
            + ", "
            + str(self.protocolCreated)
        )
