from tkinter import *
from tkinter.ttk import Treeview
from faker import Faker
from database.dbManager import *
import psycopg2
import random
import classes.ClassesManager

faker = Faker()
root = Tk()
root.withdraw()


def createTeachersListGui(master):
    classesManager = classes.ClassesManager.ClassesManager()
    classesManager.connectToDb()
    newWindow = Toplevel(root)
    newWindow.title("Teachers")
    scrollbar = Scrollbar(newWindow)
    scrollbar.pack(side=RIGHT, fill=Y)
    newWindow.geometry("850x400+380+270")
    newWindow.configure(bg="bisque")
    tree = Treeview(
        newWindow, column=("c1", "c2", "c3", "c4"), show="headings", selectmode="browse"
    )
    tree["columns"] = ("1", "2", "3", "4")
    tree.heading("1", text="ID")
    tree.heading("2", text="Tytuł")
    tree.heading("3", text="Imię")
    tree.heading("4", text="Nazwisko")
    tree.configure(xscrollcommand=scrollbar.set)
    teachers = classesManager.getTeachers()["data"]
    for i in range(len(teachers)):
        tree.insert(
            "",
            "end",
            text="i",
            values=(
                str(teachers[i].id),
                str(teachers[i].degree),
                str(teachers[i].name),
                str(teachers[i].surname),
            ),
        )
    tree.pack()
    Button(
        newWindow,
        text="Close",
        height=1,
        width=10,
        command=lambda: [newWindow.destroy()],
    ).place(x=570, y=300)
    Button(
        newWindow,
        text="Wybierz",
        height=1,
        width=10,
        command=lambda: [dbmanager.getHospitations(newWindow, tree.focus())],
    ).place(x=170, y=300)
    mainloop()


def createInspectionsListGui(list):
    newWindow = Toplevel(root)
    newWindow.title("Inspections")
    scrollbar = Scrollbar(newWindow)
    scrollbar.pack(side=RIGHT, fill=Y)
    newWindow.geometry("850x400+380+270")
    newWindow.configure(bg="bisque")
    tree = Treeview(
        newWindow, column=("c1", "c2", "c3"), show="headings", selectmode="browse"
    )
    tree["columns"] = ("1", "2", "3")
    tree.heading("1", text="ID")
    tree.heading("2", text="Data")
    tree.heading("3", text="Kurs")
    tree.configure(xscrollcommand=scrollbar.set)
    for i in range(len(list)):
        tree.insert(
            "",
            "end",
            text="i",
            values=(str(list[i].id), str(list[i].date), str(list[i].subject)),
        )
    tree.pack()
    Button(
        newWindow,
        text="Close",
        height=1,
        width=10,
        command=lambda: [newWindow.destroy(), createTeachersListGui(root)],
    ).place(x=570, y=300)
    Button(
        newWindow,
        text="Wybierz",
        height=1,
        width=10,
        command=lambda: [dbmanager.getHospitations(newWindow, tree.focus())],
    ).place(x=170, y=300)
    mainloop()


if __name__ == "__main__":
    createTeachersListGui(root)
