import psycopg2
import main.database.dbCredentials as dbCredentials


class DbManager:

    def init(self):
        self.connection = None

    def isConnected(self):
        return self.connection != None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                f"host={dbCredentials.HOST} dbname={dbCredentials.DATABASE} user={dbCredentials.LOGIN} password={dbCredentials.PASSWORD}"
            )
            return True
        except UnboundLocalError:
            return False

    def close(self):
        self.connection.close()

    def checkError(self, data):
        if len(data) > 0:
            return {"code": 0, "data": data}
        return {"code": 2, "data": "ERROR - EMPTY RETURN"}

    def getTeachers(self):
        teachers = []
        try:
            cur = self.connection.cursor()
            cur.execute(
                "SELECT * FROM users WHERE discriminator = 'teacher' ORDER BY surname"
            )
            for i in cur.fetchall():
                teachers.append(
                    {
                        "id": i[0],
                        "name": i[1],
                        "surname": i[2],
                        "pesel": i[3],
                        "password": i[4],
                        "email": i[5],
                        "lastHospitation": i[6],
                        "degree": i[7],
                        "wzhz": i[8],
                        "cathedral": i[9],
                    }
                )
        except psycopg2.Error as error:
            self.connection.rollback()
        finally:
            self.connection.commit()
        return self.checkError(teachers)

    def getHospitations(self):
        hospitations = []
        try:
            cur = self.connection.cursor()
            cur.execute(f"SELECT * FROM hospitations")
            for i in cur.fetchall():
                hospitations.append(
                    {
                        "id": i[0],
                        "userID_fk": i[1],
                        "classID_fk": i[2],
                        "scheduleID_fk": i[3],
                        "date": i[4],
                        "commission": i[5],
                        "protocolCreated": i[6],
                    }
                )
        except psycopg2.Error as error:
            self.connection.rollback()
        finally:
            self.connection.commit()
        return self.checkError(hospitations)

    def getTeachersClasses(self):
        classes = {}
        try:
            cur = self.connection.cursor()
            cur.execute(f"SELECT * FROM Users_Classes")
            for i in cur.fetchall():
                if i[0] in classes:
                    classes[i[0]].append(i[1])
                else:
                    classes[i[0]] = [i[1]]
        except psycopg2.Error as error:
            self.connection.rollback()
        finally:
            self.connection.commit()
        return self.checkError(classes)

    def getClasses(self):
        classes = []
        try:
            cur = self.connection.cursor()
            cur.execute(f"SELECT * FROM classes ORDER BY ClassName")
            for i in cur.fetchall():
                classes.append(
                    {
                        "id": i[0],
                        "className": i[1],
                        "classCode": i[2],
                        "building": i[3],
                        "room": i[4],
                        "classTime": i[5],
                        "form": i[6],
                        "studentsNum": i[7],
                    }
                )
        except psycopg2.Error as error:
            self.connection.rollback()
        finally:
            self.connection.commit()
        return self.checkError(classes)

    def getSemesters(self):
        semesters = []
        try:
            cur = self.connection.cursor()
            cur.execute(f"SELECT * FROM semesters")
            for i in cur.fetchall():
                semesters.append({"id": i[0], "startDate": i[1], "endDate": i[2]})
        except psycopg2.Error as error:
            self.connection.rollback()
        finally:
            self.connection.commit()
        return self.checkError(semesters)

    def getSchedules(self):
        schedules = []
        try:
            cur = self.connection.cursor()
            cur.execute(f"SELECT * FROM schedules")
            for i in cur.fetchall():
                schedules.append(
                    {"id": i[0], "creationDate": i[1], "semesterID_fk": i[2]}
                )
        except psycopg2.Error as error:
            self.connection.rollback()
        finally:
            self.connection.commit()
        return self.checkError(schedules)

    def getProtocols(self):
        protocols = []
        try:
            cur = self.connection.cursor()
            cur.execute(f"SELECT * FROM protocols")
            for i in cur.fetchall():
                protocols.append(
                    {  # zmienic index od i o jedno w dół
                        "id": i[0],
                        "HospitationID_fk": i[2],
                        "CreationDate": i[3],
                        "Rating": i[4],
                        "Appeal": i[5],
                    }
                )
        except psycopg2.Error as error:
            self.connection.rollback()
        finally:
            self.connection.commit()
        return self.checkError(protocols)

    def insertProtocol(self, hospitationId, creationDate, rating, appeal=False):
        try:
            cur = self.connection.cursor()
            cur.execute(
                "INSERT INTO protocols (UserID_fk, HospitationID_fk, creationdate, rating, appeal ) \
                             VALUES (%s, %s, %s, %s, %s)",
                (1, hospitationId.id, creationDate, rating, appeal),
            )
        except psycopg2.Error as error:
            self.connection.rollback()
        finally:
            self.connection.commit()

    def updateHospitationProtocol(self, hospitationId):
        try:
            cur = self.connection.cursor()
            cur.execute(
                "UPDATE hospitations SET protocolcreated=%s WHERE id=%s",
                (True, hospitationId),
            )
        except psycopg2.Error as error:
            self.connection.rollback()
        finally:
            self.connection.commit()

    def updateHospitation(self, id, teacherId, classId, commisssion):
        try:
            cur = self.connection.cursor()
            cur.execute(
                "UPDATE hospitations SET UserID_fk = %s, ClassID_fk = %s, Commission = %s WHERE id = %s",
                (
                    teacherId,
                    classId,
                    commisssion,
                    id,
                ),
            )
        except psycopg2.Error as error:
            self.connection.rollback()
        finally:
            self.connection.commit()

    def deleteHospitation(self, id):
        try:
            cur = self.connection.cursor()
            cur.execute(
                "DELETE FROM hospitations WHERE id = %s",
                (id,),
            )
            return 0
        except psycopg2.Error as error:
            self.connection.rollback()
            return -1
        finally:
            self.connection.commit()

    def insertHospitation(
        self, teacherId, classId, scheduleId, date, commission, protocolCreated
    ):
        try:
            cur = self.connection.cursor()
            cur.execute(
                "INSERT INTO hospitations (UserID_fk, ClassID_fk, ScheduleID_fk, date, commission, protocolcreated)\
                             VALUES (%s, %s, %s, %s, %s, %s)",
                (teacherId, classId, scheduleId, date, commission, protocolCreated),
            )
            cur.execute("SELECT MAX(id) FROM hospitations")
            return cur.fetchall()[0][0]
        except BaseException as error:
            print(error)
            self.connection.rollback()
            return -1
        finally:
            self.connection.commit()

    def updateProtocol(self, protocolId):
        try:
            cur = self.connection.cursor()
            cur.execute(
                "UPDATE protocols SET appeal=True WHERE id = %s",
                (
                    str(protocolId),
                ),
            )
        except psycopg2.Error as error:
            self.connection.rollback()
        finally:
            self.connection.commit()