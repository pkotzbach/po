import dbm
import tkinter

import classes.Teacher
import psycopg2
import classes.Hospitation
import database.dbCredentials as dbCredentials


class DbManager:
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                f"host={dbCredentials.HOST} dbname={dbCredentials.DATABASE} user={dbCredentials.LOGIN} password={dbCredentials.PASSWORD}"
            )
            return True
        except UnboundLocalError:
            return False

    def getTeachers(self):
        teachers = []
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT * FROM users WHERE discriminator = 'teacher'")
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
        return teachers

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
        return hospitations

    def getClasses(self):
        classes = []
        try:
            cur = self.connection.cursor()
            cur.execute(f"SELECT * FROM classes")
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
        return classes

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
        return semesters

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
        return schedules
