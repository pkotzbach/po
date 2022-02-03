import datetime

from main.classes.Protocol import Protocol
from main.classes.Schedule import Schedule
from main.classes.Class import Class
from main.classes.Teacher import Teacher
from main.classes.Hospitation import Hospitation
from main.classes.ClassesManager import ClassesManager
import main.logic.operations
import pytest

@pytest.fixture()
def hospitations():
    teacher1 = Teacher(id=1, name="Michał", surname="Abacki", pesel="", password="", email="", lastHosp="", degree="",
                       wzhz=False, cathedral="")
    teacher2 = Teacher(id=2, name="Adam", surname="Nowak", pesel="", password="", email="", lastHosp="", degree="",
                       wzhz=True, cathedral="")
    teacher3 = Teacher(id=3, name="Michał", surname="Kownacki", pesel="", password="", email="", lastHosp="", degree="",
                       wzhz=False, cathedral="")

    clas1 = Class(id=1, name="PO", code="ABC", building="", room="", time="", studentsNum="", form="")
    clas2 = Class(id=2, name="JS", code="DEF", building="", room="", time="", studentsNum="", form="")
    schedule = Schedule(id=1, creationDate="", semester="")
    teacher1.classes = [clas1, clas2]

    hospitations = []
    hosp1 = Hospitation(1, teacher1, clas1, commission=[teacher2, teacher3], schedule=schedule)
    hosp2 = Hospitation(41, teacher1, clas2, commission=[teacher2, teacher3], schedule=schedule)
    hospitations.append(hosp1)
    hospitations.append(hosp2)

    return hospitations

def test_operations_count_teacher_hospitations_number(hospitations):
    result = main.logic.operations.getHospNum(hospitations[0].id, hospitations)
    assert result == 2

def test_check_get_hospitation_protocol_exists(hospitations):
    cMan = ClassesManager()
    cMan.connectToDb()
    cMan.pullFromDatabase()
    result = cMan.getHospProtocol(hospitations[0].id)
    assert result != None
    result2 = cMan.getHospProtocol(hospitations[1].id)
    assert result2 == None

@pytest.fixture()
def protocol():
    hosp = Hospitation(
        1, "", "", commission=[], schedule=""
    )

    date = "2021-11-22"
    rating = [4.0,"Nie dotyczy",3.0,3.0,4.5,5.5,5.0,2.0,4.0]
    prot = []
    prot1 = Protocol(
        1, hosp, date, rating, False
    )
    prot.append(prot1)
    return prot

def test_operations_count_end_mark_of_protocol_id_1(protocol):
    result = main.logic.operations.getMark(1, protocol)
    assert result == round(float(31/8), 2)

def test_check_protocol_to_make_exists():
    cMan = ClassesManager()
    cMan.connectToDb()
    cMan.pullFromDatabase()
    result = cMan.getTeacherProtocolsToMake(6)
    assert result != None
    assert len(result) == 1

def test_get_teacher_correct_data():
    cMan = ClassesManager()
    cMan.connectToDb()
    cMan.pullFromDatabase()
    result = cMan.getTeacher(1).getFullName()
    assert result != None
    assert result == "dr inz. Jan Dzban"


def test_check_correct_hospitation_acquired():
    cMan = ClassesManager()
    cMan.connectToDb()
    cMan.pullFromDatabase()
    result = cMan.getHospData(5)
    assert result != None
    assert result.id == 5
    assert result.date == datetime.date(2016, 5, 22)
    assert result.clas.name == "Analiza matematyczna"