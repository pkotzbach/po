from classes.Schedule import Schedule
from classes.Teacher import Teacher
from classes.Hospitation import Hospitation
from classes.Semester import Semester
from classes.Class import Class
import database.dbManager


class ClassesManagerError:
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class ClassesManager:
    def __init__(self):
        self.dbManager = database.dbManager.DbManager()

    def connectToDb(self):
        result = self.dbManager.connect()
        if result == True:
            return {"code": 0, "data": "Polaczono z baza danych"}
        return {"code": 1, "data": "BLAD LACZENIA Z BAZA DANYCH"}

    def checkError(self, data):
        if len(data) > 0:
            return {"code": 0, "data": data}
        return {"code": 2, "data": "ERROR - EMPTY RETURN"}

    def getWithId(self, array, id):
        for element in array:
            if element.id == id:
                return element
        return None

    def pullFromDatabase(self):
        self.teachers = self.generateTeachers()
        print("pulled teachers")
        self.classes = self.generateClasses()
        print("pulled classes")
        self.semesters = self.generateSemesters()
        print("pulled semesters")
        self.schedules = self.generateSchedules()
        print("pulled schedules")
        self.hospitations = self.generateHospitations()
        print("pulled hospitations")

    def __getTeachers(self):
        data = self.dbManager.getTeachers()
        return self.checkError(data)

    def generateTeachers(self):
        teachersFromDb = self.__getTeachers()
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

    def __getSemesters(self):
        data = self.dbManager.getSemesters()
        return self.checkError(data)

    def generateSemesters(self):
        semestersFromDb = self.__getSemesters()
        semestersList = []
        if semestersFromDb["code"] != 0:
            return None

        data = semestersFromDb["data"]
        for semester in data:
            semestersList.append(
                Semester(semester["id"], semester["startDate"], semester["endDate"])
            )

        return semestersList

    def __getSchedules(self):
        data = self.dbManager.getSchedules()
        return self.checkError(data)

    def generateSchedules(self):
        schedulesFromDb = self.__getSchedules()
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

    def __getHospitations(self):
        data = self.dbManager.getHospitations()
        return self.checkError(data)

    def generateHospitations(self):
        hospsFromDb = self.__getHospitations()
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
                teacher = self.getWithId(self.teachers, teacherID)
                if teacher == None:
                    raise ClassesManagerError(f"no teacher with id {teacherID}")
                else:
                    commission.append(teacher)

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

    def __getClasses(self):
        data = self.dbManager.getClasses()
        return self.checkError(data)

    def generateClasses(self):
        classesFromDb = self.__getClasses()
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

    def getHospsForSchedule(self, scheduleId):
        # if self.teachers == or self.semesters or self.schedules

        hospsForSchedule = []
        for hosp in self.hospitations:
            if hosp.schedule.id == scheduleId:
                hospsForSchedule.append(hosp)

        return hospsForSchedule if len(hospsForSchedule) > 0 else None
