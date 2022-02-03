from main.classes import Protocol
from datetime import date

def getMark(hospId, protocols):
        for prot in protocols:
            if prot.hospitation.id == hospId:
                mark = 0.0
                counter = 0
                for i in prot.rating:
                    if i != "Nie dotyczy":
                        mark += float(i)
                        counter += 1
                mark = round(mark / float(counter), 2)
                return mark
        return None

# def insertProtocol(hospitation, boxes, classManager):
#     ranking = []
#     for i in range(1, len(boxes) + 1):
#         if (boxes["string{0}".format(i)].get() == ""):
#             return False
#         ranking.append(boxes["string{0}".format(i)].get())
#     protocol = Protocol.Protocol(0, hospitation, date.today(), ranking)
#     classManager.insertProtocol(protocol)
#     return True

def getHospNum(teacherId, hospitations):
        teacherHospNum = 0
        for hosp in hospitations:
            if hosp.teacher.id == teacherId:
                teacherHospNum += 1

        return teacherHospNum