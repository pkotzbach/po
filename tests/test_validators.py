from main.classes.Schedule import Schedule
import pytest
from main.classes.Class import Class
from main.classes.Teacher import Teacher
from main.classes.Hospitation import Hospitation
from main.logic.Validators import checkHospitation


@pytest.fixture()
def hospitation():
    teacher1 = Teacher(id=1, name="Jan", surname="Dzban", pesel="", password="", email="", lastHosp="", degree="",
                       wzhz=False, cathedral="")
    teacher2 = Teacher(id=2, name="Ania", surname="Bania", pesel="", password="", email="", lastHosp="", degree="",
                       wzhz=True, cathedral="")
    teacher3 = Teacher(id=3, name="Marek", surname="Korek", pesel="", password="", email="", lastHosp="", degree="",
                       wzhz=False, cathedral="")


    clas = Class(id=1, name="PO", code="ABC", building="", room="", time="", studentsNum="", form="")
    schedule = Schedule(id=1, creationDate="", semester="")
    teacher1.classes = [clas]

    hosp = Hospitation(
        1, teacher1, clas, commission=[teacher2, teacher3], schedule=schedule
    )
    return hosp


def test_validators_should_return_code_0_when_everything_good(hospitation):
    result = checkHospitation(hospitation)
    assert result["code"] == 0
    assert result["data"] == ""


def test_validators_should_return_code_1_when_not_all_fields_are_filled(hospitation):
    hospitation.schedule = None
    result = checkHospitation(hospitation)
    assert result["code"] == 1
    assert result["data"] == "Wszystkie pola musza byc uzupelnione"


def test_validators_should_return_code_1_when_teacher_doesnt_have_class_related_to_hospitation(
    hospitation,
):
    hospitation.teacher.classes = []
    result = checkHospitation(hospitation)
    assert result["code"] == 1
    assert result["data"] == "Nauczyciel nie uczy tego przedmiotu"


def test_validators_should_return_code_1_when_commission_size_is_smaller_than_2(
    hospitation,
):
    hospitation.commission.pop()
    result = checkHospitation(hospitation)
    assert result["code"] == 1
    assert result["data"] == "W komisji musi byc co najmniej dwoch nauczycieli"


def test_validators_should_return_code_1_when_commission_have_two_same_teachers(
    hospitation,
):
    hospitation.commission[1] = hospitation.commission[0]
    result = checkHospitation(hospitation)
    assert result["code"] == 1
    assert result["data"] == "W komisji jest co najmniej dwoch tych samych nauczycieli"


def test_validators_should_return_code_1_when_teacher_is_in_commission(
    hospitation,
):
    hospitation.teacher = hospitation.commission[0]
    result = checkHospitation(hospitation)
    assert result["code"] == 1
    assert result["data"] == "Nauczyciel hospitowany nie moze byc w komisji"


def test_validators_should_return_code_1_when_no_teacher_in_commission_is_wzhz(
    hospitation,
):
    hospitation.commission[0].wzhz = False
    result = checkHospitation(hospitation)
    assert result["code"] == 1
    assert result["data"] == "Komisja musi zawierac czlonka WZHZ"
