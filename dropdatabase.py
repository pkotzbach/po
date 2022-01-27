from venv import create
import psycopg2
dbname = "po3"
user = "postgres"
password = "321jehjeh"
port = "5433"

def create_and_generate_db():

    conn = psycopg2.connect(f"host=localhost dbname=postgres port={port} user={user} password={password}")
    cur = conn.cursor()
    conn.autocommit = True

    cur.execute(f"DROP DATABASE {dbname}")
    cur.execute(f"CREATE DATABASE {dbname}")
    conn = psycopg2.connect(f"host=localhost dbname={dbname} port={port} user={user} password={password}")
    cur = conn.cursor()
    conn.autocommit = True
    cur.execute("CREATE TABLE Hospitations(ID SERIAL NOT NULL, UserID_fk int4 NOT NULL, ClassID_fk int4 NOT NULL, ScheduleID_fk \
    int4 NOT NULL, Date date NOT NULL, Commission int[] NOT NULL, ProtocolCreated boolean NOT NULL);")
    cur.execute("CREATE TABLE Protocols(ID SERIAL NOT NULL, UserID_fk int4 NOT NULL, HospitationID_fk int4 NOT NULL, CreationDate \
    date NOT NULL, Rating TEXT[] NOT NULL, Appeal boolean NOT NULL);")
    cur.execute("CREATE TABLE Subjects_cards(ID SERIAL NOT NULL, ClassID_fk int4 NOT NULL, Course varchar(255) NOT NULL, Content varchar(255) NOT NULL);")
    cur.execute("CREATE TABLE Classes(ID SERIAL NOT NULL, ClassName varchar(255) NOT NULL, ClassCode varchar(10) NOT NULL, Building varchar(255) NOT NULL, Room varchar(255) NOT NULL, ClassTime varchar(50) NOT NULL, Form varchar(30) NOT NULL, StudentsNum int4 NOT NULL);")
    cur.execute("CREATE TABLE Users(ID SERIAL NOT NULL, Name varchar(255) NOT NULL, Surname varchar(255) NOT NULL, Pesel varchar(255) NOT NULL, Password varchar(255) NOT NULL, Email varchar(255) NOT NULL, LastHospitation date, Degree varchar(20), Wzhz boolean, Cathedral varchar(255), Discriminator varchar(255) NOT NULL, CHECK(Discriminator LIKE 'teacher' or Discriminator LIKE 'headOfDep'));")
    cur.execute("CREATE TABLE Schedules(ID SERIAL NOT NULL, CreationDate date NOT NULL, SemesterID_fk int4 NOT NULL);")
    cur.execute("CREATE TABLE Semesters(ID SERIAL NOT NULL, StartDate date NOT NULL, EndDate date NOT NULL);")
    cur.execute("CREATE TABLE Hospitations_Users(HospitationID_fk int4 NOT NULL, UserID_fk int4 NOT NULL);")
    cur.execute("CREATE TABLE Users_Classes(UserID_fk int4 NOT NULL, ClassID_fk int4 NOT NULL);")

    cur.execute("ALTER TABLE Hospitations ADD PRIMARY KEY(ID);")
    cur.execute("ALTER TABLE Protocols ADD PRIMARY KEY(ID);")
    cur.execute("ALTER TABLE Subjects_cards ADD PRIMARY KEY(ID);")
    cur.execute("ALTER TABLE Classes ADD PRIMARY KEY(ID);")
    cur.execute("ALTER TABLE Users ADD PRIMARY KEY(ID);")
    cur.execute("ALTER TABLE Schedules ADD PRIMARY KEY(ID);")
    cur.execute("ALTER TABLE Semesters ADD PRIMARY KEY(ID);")
    cur.execute("ALTER TABLE Hospitations_Users ADD PRIMARY KEY(HospitationID_fk, UserID_fk);")
    cur.execute("ALTER TABLE Users_Classes ADD PRIMARY KEY(UserID_fk, ClassID_fk);")

    cur.execute("ALTER TABLE Subjects_cards ADD CONSTRAINT subject_card_class_con FOREIGN KEY(ClassID_fk) REFERENCES Classes(ID);")
    cur.execute("ALTER TABLE Hospitations_Users ADD CONSTRAINT hosp_user_hosp_con FOREIGN KEY(HospitationID_fk) REFERENCES Hospitations(ID);")
    cur.execute("ALTER TABLE Hospitations_Users ADD CONSTRAINT hosp_user_user_con FOREIGN KEY(UserID_fk) REFERENCES Users(ID);")
    cur.execute("ALTER TABLE Users_Classes ADD CONSTRAINT user_class_user_con FOREIGN KEY(UserID_fk) REFERENCES Users(ID);")
    cur.execute("ALTER TABLE Users_Classes ADD CONSTRAINT user_class_class_con FOREIGN KEY(ClassID_fk) REFERENCES Classes(ID);")
    cur.execute("ALTER TABLE Hospitations ADD CONSTRAINT hospitation_schedule_con FOREIGN KEY(ScheduleID_fk) REFERENCES Schedules(ID);")
    cur.execute("ALTER TABLE Protocols ADD CONSTRAINT protocol_hosp_con FOREIGN KEY(HospitationID_fk) REFERENCES Hospitations(ID);")
    cur.execute("ALTER TABLE Protocols ADD CONSTRAINT protocol_user_con FOREIGN KEY(UserID_fk) REFERENCES Users(ID);")
    cur.execute("ALTER TABLE Hospitations ADD CONSTRAINT protocol_class_con FOREIGN KEY(ClassID_fk) REFERENCES Classes(ID);")
    cur.execute("ALTER TABLE Schedules ADD CONSTRAINT semester_schedule_con FOREIGN KEY(SemesterID_fk) REFERENCES Semesters(ID);")
    cur.execute("ALTER TABLE Hospitations ADD CONSTRAINT hosp_user_con FOREIGN KEY(UserID_fk) REFERENCES Users(ID);")

    conn.close()

create_and_generate_db()