from main.classes.ClassesManager import ClassesManager

def test_get_teacher_hosp_return_none():
    cMan = ClassesManager()
    cMan.connectToDb()
    cMan.pullFromDatabase()
    teacherId = -1
    result = cMan.getTeacherHosp(teacherId)
    assert result == None
    cMan.closeConnection()

def test_get_teacher_hosp_return_more_than_zero_or_equal():
    cMan = ClassesManager()
    cMan.connectToDb()
    cMan.pullFromDatabase()
    teacherId = 1
    result = cMan.getTeacherHosp(teacherId)
    assert len(result) >= 0
    cMan.closeConnection()


def test_get_protocol_from_hosp_return_none():
    cMan = ClassesManager()
    cMan.connectToDb()
    cMan.pullFromDatabase()
    hospId = -1
    result = cMan.getHospProtocol(hospId)
    assert result == None
    cMan.closeConnection()

def test_get_protocol_from_hosp_return_prot():
    cMan = ClassesManager()
    cMan.connectToDb()
    cMan.pullFromDatabase()
    hospId = 38
    result = cMan.getHospProtocol(hospId)
    assert result != None
    assert result.hospitation.id == hospId
    cMan.closeConnection()