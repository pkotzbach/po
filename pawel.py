from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style, Combobox
from turtle import left
from faker import Faker
import classes.ClassesManager
import psycopg2
import random


class ScheduleGui:
    def __init__(self):
        self.classesManager = classes.ClassesManager.ClassesManager()
        result = self.classesManager.connectToDb()
        self.classesManager.pullFromDatabase()
        # messagebox.showinfo("Database", result["data"])

        self.root = Tk()
        self.root.withdraw()
        self.window = Toplevel(self.root)
        self.window.title("Schedule")
        self.window.geometry("850x400+380+270")
        self.window.configure(bg="bisque")
        self.style = Style()
        self.style.theme_use("classic")
        self.style.configure("Treeview", rowheight=80)

    def end(self):
        self.window.destroy()
        exit()

    def fillTree(self, hospitations, tree):
        tree.delete(*tree.get_children())
        if hospitations != None:
            for hosp in hospitations:
                comission = ""
                for teacher in hosp.commission:
                    comission += teacher.getFullName() + "\n"
                tree.insert(
                    "",
                    "end",
                    text="i",
                    values=(
                        str(hosp.clas.name + "\n" + hosp.clas.code),
                        hosp.teacher.getFullName(),
                        hosp.clas.time,
                        comission,
                    ),
                )
        else:
            # TODO: chyba jest git, chociaz w specyfikacji bylo, ze ma sie wyswietlic "Brak hospitacji"
            # tree.insert(
            #     "",
            #     "end",
            #     text="i",
            # )
            pass

    def createSchedule(self):
        scheduleFrame = Frame(self.window)
        tree = Treeview(scheduleFrame, show="headings", selectmode="browse", height=3)
        tree["columns"] = ("1", "2", "3", "4")
        tree.column("1", width=200)
        tree.column("2", width=150)
        tree.column("3", width=150)
        tree.column("4", width=300)
        tree.heading("1", text="Nazwa i kod kursu")
        tree.heading("2", text="Dane hospitowanego")
        tree.heading("3", text="Miejsce i termin zajec")
        tree.heading("4", text="Dane zespolu hospitujacego")
        scrollbar = Scrollbar(scheduleFrame, command=tree.yview, orient=VERTICAL)
        tree.configure(yscrollcommand=scrollbar.set)

        hospitations = self.classesManager.getHospsForSchedule(1)
        self.fillTree(hospitations, tree)

        # if semesters = None?

        combobox = Combobox(scheduleFrame, width=40)
        combobox["values"] = [
            schedule.semester.range() for schedule in self.classesManager.schedules
        ]
        combobox.current(0)

        def scheduleChange(event):
            self.fillTree(
                self.classesManager.getHospsForSchedule(combobox.current() + 1), tree
            )

        combobox.bind("<<ComboboxSelected>>", scheduleChange)

        combobox.pack(anchor=NW)
        scheduleFrame.pack()
        tree.pack(side=LEFT)
        scrollbar.pack(side=LEFT, fill=Y)

        Button(
            self.window,
            text="Close",
            height=1,
            width=10,
            command=lambda: [self.end()],
        ).place(x=570, y=300)

        # Button(
        #     self.window,
        #     text="Edit",
        #     height=1,
        #     width=10,
        #     command=lambda: [],
        # ).place(x=370, y=300)

        # Button(
        #     self.window,
        #     text="Add",
        #     height=1,
        #     width=10,
        #     command=lambda: [end()],
        # ).place(x=170, y=300)

        mainloop()


if __name__ == "__main__":
    scheduleGui = ScheduleGui()
    scheduleGui.createSchedule()
