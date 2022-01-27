import psycopg2
import random
from faker import Faker

CLASSES_AMMOUNT = 20
USERS_AMMOUNT = 40
HOSP_AMMOUNT = 40
USERS_CLASSES_AMMOUNT = 20
HOSPITATIONS_USER_AMMOUNT = 20
YEARS_AMMOUNT = 5 + 10  # +10 bo zaczynamy od 10

faker = Faker()

host = "abul.db.elephantsql.com"
port = "5432"
dbname = "uyqavgoj"
dbuser = "uyqavgoj"
password = "KP3nHqYmwHhlNkb_BA3fXYASxO3ugs-E"


def classes():
    # wtasowanie zajęć
    conn = psycopg2.connect(
        f"host={host} port={port} dbname={dbname} user={dbuser} password={password}"
    )
    cur = conn.cursor()
    cname = [
        "Architektura komputerów",
        "Analiza matematyczna",
        "Fizyka",
        "Języki skrytpowe",
        "Cyberbezpieczeństwo",
        "Statystyka",
    ]
    code = ["L", "P", "W"]
    b = [
        "A-1",
        "A-4",
        "B-1",
        "B-2",
        "C-13",
        "C-3",
        "D-1",
        "D-2",
        "D-4",
        "A-2",
        "B-6",
        "C-6",
    ]
    cla = ["122", "101", "112", "223", "222", "256", "115", "222a"]
    t = [
        "poniedziałek, 13:15-15:00",
        "poniedziałek, 15:15-17:00",
        "wtorek, 11:15-13:00",
        "wtorek, 9:15-11:00",
        "środa, 13:15-15:00",
        "czwartek, 15:15-17:00",
        "piątek, 13:15-15:00",
        "piątek, 9:15-11:00",
    ]
    form = [
        "I stopień, stacjonarne",
        "II stopień, stacjonarne",
        "I stopień, niestacjonarne",
        "II stopień, niestacjonarne",
    ]
    for i in range(CLASSES_AMMOUNT):
        c = "INZ"
        for i in range(6):
            c += str(random.randint(0, 9))
        c += random.choice(code)
        cur.execute(
            "INSERT INTO classes (classname, classcode, building, room, classtime, form, studentsnum) \
        VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                random.choice(cname),
                c,
                random.choice(b),
                random.choice(cla),
                random.choice(t),
                random.choice(form),
                random.randint(15, 30),
            ),
        )
    conn.commit()


# # ---------------------------------------------------------------------------------------
# #wtasowanie uzytkownikow
def users():
    degree = ["mgr inz.", "dr hab. inz.", "dr inz.", "prof. dr hab. inż."]
    catherdrals = [
        "Katedra Automatyki, Mechatroniki i Systemów Sterowania ",
        "Katedra Systemów i Sieci Komputerowych",
        "Katedra Informatyki i Inżynierii Systemów",
        "Katedra Informatyki Stosowanej",
        "Katedra Podstaw Informatyki",
    ]
    conn = psycopg2.connect(
        f"host={host} port={port} dbname={dbname} user={dbuser} password={password}"
    )
    cur = conn.cursor()
    for i in range(USERS_AMMOUNT):
        if i % 7 == 0:
            cur.execute(
                "INSERT INTO users (name, surname, pesel, password, email, cathedral, discriminator) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    faker.first_name(),
                    faker.last_name(),
                    str(random.randint(1000000000, 9999999999))[1:],
                    faker.password(),
                    faker.email(),
                    random.choice(catherdrals),
                    "headOfDep",
                ),
            )
        else:
            cur.execute(
                "INSERT INTO users (name, surname, pesel, password, email, lasthospitation, \
                 degree, wzhz, cathedral, discriminator) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    faker.first_name(),
                    faker.last_name(),
                    str(random.randint(1000000000, 9999999999))[1:],
                    faker.password(),
                    faker.email(),
                    faker.date(),
                    random.choice(degree),
                    random.choice([True, False]),
                    random.choice(catherdrals),
                    "teacher",
                ),
            )
    conn.commit()


# -----------------------
# wtasowanie hospitacji
def hosp():
    conn = psycopg2.connect(
        f"host={host} port={port} dbname={dbname} user={dbuser} password={password}"
    )
    cur = conn.cursor()
    teachersId = []
    classesId = []
    schedulesId = []
    teachersIdwzhz = []

    cur.execute("SELECT * FROM users WHERE wzhz = 't'")
    list = cur.fetchall()
    for i in range(len(list)):
        teachersIdwzhz.append(list[i][0])

    cur.execute("SELECT * FROM schedules")
    list = cur.fetchall()
    for i in range(len(list)):
        schedulesId.append(list[i][0])

    cur.execute("SELECT * FROM users_classes")
    list = cur.fetchall()
    for i in range(len(list)):
        teachersId.append(list[i][0])
        classesId.append(list[i][1])

    for i in range(HOSP_AMMOUNT):
        com = []
        for i in range(random.randint(2, 5)):
            com.append(random.choice(teachersIdwzhz))
        cur.execute(
            "INSERT INTO hospitations (UserID_fk, ClassID_fk, ScheduleID_fk , date, commission, protocolcreated) \
                     VALUES (%s, %s, %s, %s, %s, %s)",
            (
                random.choice(teachersId),
                random.choice(classesId),
                random.choice(schedulesId),
                faker.date(),
                com,
                random.choice([True, False]),
            ),
        )

    conn.commit()


# -------------------------------------------------------------------------------------------------------


def usersclasses():
    # users_classes
    conn = psycopg2.connect(
        f"host={host} port={port} dbname={dbname} user={dbuser} password={password}"
    )
    cur = conn.cursor()

    for i in range(1, USERS_CLASSES_AMMOUNT):
        user = random.randint(1, USERS_AMMOUNT)
        clas = random.randint(1, CLASSES_AMMOUNT)
        try:
            cur.execute(
                "INSERT INTO Users_Classes (UserID_fk, ClassID_fk) \
                        VALUES (%s, %s)",
                (user, clas),
            )
        except psycopg2.errors.UniqueViolation:
            continue

    conn.commit()


def hospusers():
    conn = psycopg2.connect(
        f"host={host} port={port} dbname={dbname} user={dbuser} password={password}"
    )
    cur = conn.cursor()

    for i in range(1, HOSPITATIONS_USER_AMMOUNT):
        hosp = random.randint(1, HOSP_AMMOUNT)
        user = random.randint(1, USERS_AMMOUNT)
        try:
            cur.execute(
                "INSERT INTO Hospitations_Users (HospitationID_fk, UserID_fk) \
                        VALUES (%s, %s)",
                (hosp, user),
            )
        except psycopg2.errors.UniqueViolation:
            continue

    conn.commit()


def semesters():
    # semesters
    conn = psycopg2.connect(
        f"host={host} port={port} dbname={dbname} user={dbuser} password={password}"
    )
    cur = conn.cursor()

    for i in range(10, YEARS_AMMOUNT):
        cur.execute(
            "INSERT INTO Semesters (StartDate, EndDate) \
                        VALUES (%s, %s)",
            (f"20{i}-03-01", f"20{i}-06-01"),
        )
        cur.execute(
            "INSERT INTO Semesters (StartDate, EndDate) \
                        VALUES (%s, %s)",
            (f"20{i}-10-01", f"20{i+1}-02-01"),
        )

    conn.commit()


def schedules():
    conn = psycopg2.connect(
        f"host={host} port={port} dbname={dbname} user={dbuser} password={password}"
    )
    cur = conn.cursor()

    for i in range(1, 1 + (YEARS_AMMOUNT - 10) * 2):
        cur.execute(
            "INSERT INTO Schedules (CreationDate, SemesterID_fk) \
                        VALUES (%s, %s)",
            (f"2010-01-01", i),
        )

    conn.commit()


classes()
users()
usersclasses()
semesters()
schedules()
hosp()
hospusers()
