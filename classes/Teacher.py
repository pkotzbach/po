import datetime


class Teacher:
    def __init__(
        self,
        id,
        name,
        surname,
        pesel,
        password,
        email,
        lastHosp: datetime.datetime,
        degree,
        wzhz,
        cathedral,
    ):
        self.id = id
        self.name = name
        self.surname = surname
        self.pesel = pesel
        self.password = password
        self.email = email
        self.lastHospitation = lastHosp
        self.degree = degree
        self.wzhz = wzhz
        self.cathedral = cathedral

    def getFullName(self):
        return self.degree + " " + self.name + " " + self.surname
