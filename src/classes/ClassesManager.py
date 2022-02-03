from datetime import date

from main.classes.Protocol import Protocol
from main.classes.Schedule import Schedule
from main.classes.Teacher import Teacher
from main.classes.Hospitation import Hospitation
from main.classes.Semester import Semester
from main.classes.Class import Class
import main.database.dbManager


class ClassesManagerError(BaseException):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class ClassesManager:
    def __init__(self):
        self.dbManager = main.database.dbManager.DbManager()

    def _dbManager(func):
        def wrapper(*args):
            self = args[0]
            if self.dbManager.isConnected() == False:
                raise ClassesManagerError("dbManager not connected!")
            return func(*args)

        return wrapper

    def connectToDb(self):
        result = self.dbManager.connect()
        if result == True:
            return {"code": 0, "data": "Polaczono z baza danych"}
        return {"code": 1, "data": "BLAD LACZENIA Z BAZA DANYCH"}

    @_dbManager
    def closeConnection(self):
        self.dbManager.close()

    def getWithId(self, array, id):
        for element in array:
            if element.id == id:
                return element
        return None

    @_dbManager
    def pullFromDatabase(self):
        self.teachers = self.generateTeachers()
        #print(f"pulled {len(self.teachers)} teachers")
        self.classes = self.generateClasses()
        #print(f"pulled {len(self.classes)} classes")
        self.semesters = self.generateSemesters()
        #print(f"pulled {len(self.semesters)} semesters")
        self.schedules = self.generateSchedules()
        #print(f"pulled {len(self.schedules)} schedules")
        self.hospitations = self.generateHospitations()
        #print(f"pulled {len(self.hospitations)} hospitations")
        self.protocols = self.generateProtocols()
        #print(f"pulled {len(self.protocols)} protocols")
        classesForTeacher = self.addClassesForTeacher()
        #print(f"pulled {len(classesForTeacher)} teachers' classes")

    @_dbManager
    def generateTeachers(self):
        teachersFromDb = self.dbManager.getTeachers()
        teachersList = []
        if teachersFromDb["code"] != 0:
            return None

        data = teachersFromDb["data"]
        for teacher in data:
            teachersList.append(
                Teacher(
                    teacher["id"],
                    teacher["name"],
                    teacher["surname"],
                    teacher["pesel"],
                    teacher["password"],
                    teacher["email"],
                    teacher["lastHospitation"],
                    teacher["degree"],
                    teacher["wzhz"],
                    teacher["cathedral"],
                )
            )

        return teachersList

    @_dbManager
    def addClassesForTeacher(self):
        tClassesFromDb = self.dbManager.getTeachersClasses()
        if tClassesFromDb["code"] != 0:
            return None

        data = tClassesFromDb["data"]
        for teacher in self.teachers:
            if teacher.id in data:
                for clasId in data[teacher.id]:
                    teacher.classes.append(self.getWithId(self.classes, clasId))

        return data

    @_dbManager
    def generateSemesters(self):
        semestersFromDb = self.dbManager.getSemesters()
        semestersList = []
        if semestersFromDb["code"] != 0:
            return None

        data = semestersFromDb["data"]
        for semester in data:
            semestersList.append(
                Semester(semester["id"], semester["startDate"], semester["endDate"])
            )

        return semestersList

    @_dbManager
    def generateSchedules(self):
        schedulesFromDb = self.dbManager.getSchedules()
        schedulesList = []
        if schedulesFromDb["code"] != 0:
            return None

        data = schedulesFromDb["data"]
        for schedule in data:
            semesterId = schedule["semesterID_fk"]
            semester = self.getWithId(self.semesters, semesterId)
            if semester == None:
                raise ClassesManagerError(f"no semester with id {semesterId}")

            schedulesList.append(
                Schedule(
                    schedule["id"],
                    schedule["creationDate"],
                    semester,
                )
            )

        return schedulesList

    def updateProtocol(self, protocolId):
        result = self.dbManager.updateProtocol(protocolId)

    @_dbManager
    def generateHospitations(self):
        hospsFromDb = self.dbManager.getHospitations()
        hospsList = []
        if hospsFromDb["code"] != 0:
            return None

        data = hospsFromDb["data"]
        for hosp in data:
            teacherID = hosp["userID_fk"]
            teacher = self.getWithId(self.teachers, teacherID)
            if teacher == None:
                raise ClassesManagerError(f"no teacher with id {teacherID}")

            classID = hosp["classID_fk"]
            clas = self.getWithId(self.classes, classID)
            if clas == None:
                raise ClassesManagerError(f"no user with id {classID}")

            scheduleID = hosp["scheduleID_fk"]
            schedule = self.getWithId(self.schedules, scheduleID)
            if schedule == None:
                raise ClassesManagerError(f"no schedule with id {scheduleID}")

            commissionIDs = hosp["commission"]
            commission = []
            for teacherID in commissionIDs:
                teacherC = self.getWithId(self.teachers, teacherID)
                if teacherC == None:
                    raise ClassesManagerError(f"no teacher with id {teacherID}")
                else:
                    commission.append(teacherC)

            hospsList.append(
                Hospitation(
                    hosp["id"],
                    teacher,
                    clas,
                    schedule,
                    hosp["date"],
                    commission,
                    hosp["protocolCreated"],
                )
            )

        return hospsList

    @_dbManager
    def generateClasses(self):
        classesFromDb = self.dbManager.getClasses()
        classesList = []
        if classesFromDb["code"] != 0:
            return None

        data = classesFromDb["data"]
        for clas in data:
            classesList.append(
                Class(
                    clas["id"],
                    clas["className"],
                    clas["classCode"],
                    clas["building"],
                    clas["room"],
                    clas["classTime"],
                    clas["form"],
                    clas["studentsNum"],
                )
            )

        return classesList

    @_dbManager
    def generateProtocols(self):
        protocolsFromDb = self.dbManager.getProtocols()
        protocolsList = []
        if protocolsFromDb["code"] != 0:
            return None

        data = protocolsFromDb["data"]
        for prot in data:
            hospId = prot["HospitationID_fk"]
            hospit = self.getWithId(self.hospitations, hospId)
            if hospit == None:
                raise ClassesManagerError(f"no hospitation with id {hospId}")

            protocolsList.append(
                Protocol(
                    prot["id"],
                    hospit,
                    prot["CreationDate"],
                    prot["Rating"],
                    prot["Appeal"],
                )
            )
        return protocolsList

    def getHospProtocol(self, hospId):
        self.protocols = self.generateProtocols()
        for prot in self.protocols:
            if prot.hospitation.id == hospId:
                return prot
        return None

    def getTeacherHosp(self, teacherId):
        self.hospitations = self.generateHospitations()
        teacherHosp = []
        for hosp in self.hospitations:
            if hosp.teacher.id == teacherId:
                teacherHosp.append(hosp)

        return teacherHosp if len(teacherHosp) > 0 else None

    def getHospsForSchedule(self, schedule):
        self.hospitations = self.generateHospitations()
        hospsForSchedule = []
        for hosp in self.hospitations:
            if hosp.schedule == schedule:
                hospsForSchedule.append(hosp)

        return hospsForSchedule if len(hospsForSchedule) > 0 else None

    def getClassWithCode(self, code: str):
        for clas in self.classes:
            if clas.code == code:
                return clas
        return None

    def getTeacherProtocolsToMake(self, teacherId):
        self.hospitations = self.generateHospitations()
        neededProtocols = []
        for hosp in self.hospitations:
            for com in hosp.commission:
                if com.id == teacherId and hosp.protocolCreated == False:
                    neededProtocols.append(hosp)

        return neededProtocols if len(neededProtocols) > 0 else None

    def getHospData(self, hospId):
        self.hospitations = self.generateHospitations()
        for hosp in self.hospitations:
            if hosp.id == hospId:
                return hosp
        return None

    def getTeacher(self, teacherId):
        self.teachers = self.generateTeachers()
        return self.getWithId(self.teachers, teacherId)

    @_dbManager
    def replaceHosp(self, old, new):
        self.hospitations = self.generateHospitations()
        for i in range(len(self.hospitations)):
            if self.hospitations[i] == old:
                self.hospitations[i] = new
                self.dbManager.updateHospitation(
                    new.id, new.teacher.id, new.clas.id, new.commissionIds()
                )
                return True
        return False

    @_dbManager
    def insertHosp(self, hosp):
        result = self.dbManager.insertHospitation(
            hosp.teacher.id,
            hosp.clas.id,
            hosp.schedule.id,
            hosp.date,
            hosp.commissionIds(),
            hosp.protocolCreated,
        )

        if result != -1:
            hosp.id = result
            self.hospitations.append(hosp)
            return True
        return False

    @_dbManager
    def deleteHosp(self, hosp):
        result = self.dbManager.deleteHospitation(hosp.id)

        if result == 0:
            for i in range(len(self.hospitations)):
                if self.hospitations[i].id == hosp.id:
                    self.hospitations.pop(i)
                    return True
            raise ClassesManagerError("NO HOSPITATION WITH THAT ID ON LIST")
        return False

    @_dbManager
    def insertProtocol(self, hospitation, boxes):
        self.protocols = self.generateProtocols()
        self.hospitations = self.generateHospitations()
        ranking = []
        for i in boxes.values():
            if i.get() == "":
                return False
            ranking.append(i.get())
        protocol = Protocol(0, hospitation, date.today(), ranking)

        for i in self.protocols:
            if i.hospitation.id == protocol.hospitation.id:
                return False

        self.dbManager.insertProtocol(
             protocol.hospitation, protocol.date, protocol.rating, protocol.appeal
        )
        self.dbManager.updateHospitationProtocol(protocol.hospitation.id)
        self.hospitations = self.generateHospitations()
        self.protocols = self.generateProtocols()
        return True

    def getCathedralTeachers(self, inspectorId):
        self.protocols = self.generateProtocols()
        self.hospitations = self.generateHospitations()
        teachers = []
        cat = self.getTeacher(inspectorId)
        for teacher in self.teachers:
            if teacher.cathedral == cat.cathedral:
                teachers.append(teacher)
        return teachers if len(teachers) > 0 else None

