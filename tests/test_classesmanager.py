from main.classes.ClassesManager import ClassesManager

cMan = ClassesManager()
cMan.connectToDb()
cMan.pullFromDatabase()

def test_pullFromDatabase_should_fill_all_lists():
    cMan = ClassesManager()
    cMan.connectToDb()
    cMan.pullFromDatabase()
    assert cMan.classes != None
    assert cMan.teachers != None
    assert cMan.hospitations != None
    assert cMan.schedules != None
    assert cMan.protocols != None
    assert cMan.semesters != None
    cMan.closeConnection()
