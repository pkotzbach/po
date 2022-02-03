import datetime
from main.classes.Teacher import Teacher
from main.classes.Schedule import Schedule
from main.classes.Class import Class


class Hospitation:
    def __init__(
        self,
        id=-1,
        teacher: Teacher = None,
        clas: Class = None,
        schedule: Schedule = None,
        date: datetime.date = None,
        commission: list[Teacher] = [],
        protocolCreated=False,
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
            + str(self.teacher.getFullName())
            + ", "
            + str(self.clas.id)
            + ", "
            + str(self.schedule.id)
            + ", "
            + str(self.date)
            + ", "
            + str(len(self.commission))
            + ", "
            + str(self.protocolCreated)
        )

    def copy(self):
        copy = Hospitation(
            self.id,
            self.teacher,
            self.clas,
            self.schedule,
            self.date,
            [],
            self.protocolCreated,
        )

        for teacher in self.commission:
            copy.commission.append(teacher)

        return copy

    def commissionIds(self):
        return [teacher.id for teacher in self.commission]
