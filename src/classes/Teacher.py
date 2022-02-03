import datetime


class Teacher:
    def __init__(
        self,
        id,
        name: str,
        surname: str,
        pesel,
        password,
        email,
        lastHosp: datetime.datetime,
        degree: str,
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
        self.classes = []

    def getFullName(self) -> str:
        return str(self.degree) + " " + self.name + " " + self.surname

    def __str__(self) -> str:
        return self.getFullName()
