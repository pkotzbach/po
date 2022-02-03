from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style, Combobox
import menu
from main.classes.Hospitation import Hospitation
from main.logic import Validators


class ScheduleGuiException(BaseException):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class ScheduleGui:
    TEACHERS_CLASS = " - X"
    TEACHER_WZHZ = " - WZHZ"

    def __init__(self, view, cmanager):
        self.classesManager = cmanager
        self.window = view
        self.window.configure(bg="bisque")
        self.window.title("Easy Inspection")
        self.window.geometry("850x500+380+270")
        self.window.configure(bg="bisque")
        self.style = Style()
        self.style.theme_use("classic")
        self.style.configure("Treeview", rowheight=80)
        self.window.protocol("WM_DELETE_WINDOW", self.end)
        self.scheduleFrame = Frame(self.window)
        self.tree = Treeview(
            self.scheduleFrame, show="headings", selectmode="browse", height=3
        )

    def end(self):
        self.clearWhole()
        self.style.configure("Treeview", rowheight=20)
        gui = menu.Menu_GUI()
        gui.start_with_opened_window(self.window, self.classesManager)
        gui.main_window()

    def printError(self, data):
        messagebox.showerror("Error", data)

    def clearFrame(self):
        for widgets in self.scheduleFrame.winfo_children():
            widgets.destroy()

    def clearWhole(self):
        for widgets in self.window.winfo_children():
            widgets.destroy()

    def clearWindow(self):
        for widgets in self.window.winfo_children():
            if (widgets.winfo_class() != "Frame"):
                widgets.destroy()

    def fillTreeWithHosps(self, hospitations):
        self.tree.delete(*self.tree.get_children())
        if hospitations != None:
            for hosp in hospitations:
                comission = ""
                for teacher in hosp.commission:
                    comission += teacher.getFullName() + "\n"
                self.tree.insert(
                    "",
                    "end",
                    text=hosp.id,
                    values=(
                        str(hosp.clas.code + " \n" + hosp.clas.name),
                        hosp.teacher.getFullName(),
                        hosp.clas.time,
                        comission,
                    ),
                )
        else:
            pass

    def currentSchedule(self):
        return self.classesManager.schedules[self.combobox.current()]

    def scheduleChange(self, event=None):
        self.fillTreeWithHosps(
            self.classesManager.getHospsForSchedule(self.currentSchedule()),
        )

    def createSchedule(self):
        self.tree["columns"] = (
            "clas",
            "teacher",
            "place",
            "commission",
            "teacherClassManId",
            "clasClassManId",
        )
        self.tree["displaycolumns"] = (
            "clas",
            "teacher",
            "place",
            "commission",
        )
        self.tree.column("clas", width=200)
        self.tree.column("teacher", width=150)
        self.tree.column("place", width=150)
        self.tree.column("commission", width=300)
        self.tree.heading("clas", text="Nazwa i kod kursu")
        self.tree.heading("teacher", text="Dane hospitowanego")
        self.tree.heading("place", text="Miejsce i termin zajec")
        self.tree.heading("commission", text="Dane zespolu hospitujacego")
        scrollbar = Scrollbar(self.scheduleFrame, command=self.tree.yview, orient=VERTICAL)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.combobox = Combobox(self.scheduleFrame, width=40)
        self.combobox["values"] = [
            schedule.semester.range() for schedule in self.classesManager.schedules
        ]
        self.combobox.current(0)

        self.combobox.bind("<<ComboboxSelected>>", self.scheduleChange)

        self.combobox.pack(anchor=NW)
        self.scheduleFrame.pack()
        self.tree.pack(side=LEFT)
        scrollbar.pack(side=LEFT, fill=Y)

    def createCloseButton(self):
        Button(
            self.window,
            text="Wróć",
            height=1,
            width=10,
            command=lambda: [self.end()],
        ).place(x=570, y=300)

    def createEditAddButtons(self):
        Button(
            self.window,
            text="Edit",
            height=1,
            width=10,
            command=lambda: [self.editGui()],
        ).place(x=370, y=300)

        Button(
            self.window,
            text="Add",
            height=1,
            width=10,
            command=lambda: [self.addGui()],
        ).place(x=170, y=300)

    def editGui(self):
        hosp = self.classesManager.getWithId(
            self.classesManager.hospitations, self.tree.item(self.tree.focus())["text"]
        )

        if hosp != None:
            self.addEditGui(hosp.copy(), hosp)

    def addGui(self):
        hosp = Hospitation(schedule=self.currentSchedule(), commission=[])
        self.addEditGui(hosp)

    def addEditGui(self, hosp, HOSP_ORI=None):
        if hosp == None:
            raise ScheduleGuiException("hospitation need to be passed to addEditGui!")

        INPUT_WIDTH = 40
        window = Toplevel(self.window)
        window.title("Edit")
        window.geometry("500x300+380+270")
        window.configure(bg="bisque")

        Label(window, bg="bisque", text="Osoba hospitowana:").grid(row=0)
        Label(window, bg="bisque", text="Kurs:").grid(row=1)
        Label(window, bg="bisque", text="Komisja:").grid(row=5)
        Label(window, bg="bisque", text="Operacje na komisji:").grid(row=6)
        self.codeVar = StringVar()
        self.nameVar = StringVar()
        name = Combobox(window, width=INPUT_WIDTH, textvariable=self.nameVar)
        code = Combobox(window, width=INPUT_WIDTH, textvariable=self.codeVar)
        commissionLabel = Label(window, bg="bisque")
        commissionCRUD = Combobox(window, width=INPUT_WIDTH)

        def addComCallback():
            teacher = self.classesManager.teachers[commissionCRUD.current()]
            print(
                "DODANO",
                teacher.getFullName(),
            )
            hosp.commission.append(teacher)
            updateCommissionLabel()

        def deleteComCallback():
            teacher = self.classesManager.teachers[commissionCRUD.current()]
            print(
                "USUNIETO",
                teacher.getFullName(),
            )
            hosp.commission.remove(teacher)
            updateCommissionLabel()

        def deleteCallback():
            print("USUWAM Z BAZY..")
            result = self.classesManager.deleteHosp(hosp)
            if result == True:
                print("USUNIETO")
            else:
                print("BLAD")
                self.printError(
                    "Blad podczas usuwania z bazy. Prawdopodobnie hospitacja posiada protokol."
                )
            self.scheduleChange()
            window.destroy()

        def saveCallback():
            hosp.teacher = self.classesManager.teachers[name.current()]
            hosp.clas = self.classesManager.classes[code.current()]
            check = Validators.checkHospitation(hosp)
            if check["code"] == 1:
                print(check["data"])
                self.printError(check["data"])
            else:
                print("ZAPISUJE DO BAZY..")
                result = (
                    self.classesManager.replaceHosp(HOSP_ORI, hosp)
                    if HOSP_ORI != None
                    else self.classesManager.insertHosp(hosp)
                )
                if result == True:
                    print("ZAPISANO")
                else:
                    print("BLAD")
                    self.printError("Blad podczas dodawania do bazy.")
                self.scheduleChange()
                window.destroy()

        def updateCommissionLabel():
            commission = hosp.commission
            commissionText = ""

            for teacher in commission:
                commissionText += teacher.getFullName() + "\n"

            commissionLabel["text"] = commissionText

        def classesForTeacherCallback(event):
            teacher = self.classesManager.teachers[name.current()]
            code["values"] = [
                str(clas) + (self.TEACHERS_CLASS if clas in teacher.classes else "")
                for clas in self.classesManager.classes
            ]

        addCom = Button(window, text="Dodaj", command=addComCallback)
        deleteCom = Button(window, text="Usun", command=deleteComCallback)
        save = Button(window, text="Save", command=saveCallback)
        close = Button(window, text="Wróć", command=window.destroy)

        # code["values"] = [str(clas) for clas in self.classesManager.classes]

        name["values"] = [
            teacher.getFullName() for teacher in self.classesManager.teachers
        ]

        commissionCRUD["values"] = [
            teacher.getFullName() + (self.TEACHER_WZHZ if teacher.wzhz == True else "")
            for teacher in self.classesManager.teachers
        ]

        code.grid(row=1, column=1)
        name.grid(row=0, column=1)
        commissionLabel.grid(row=5, column=1)
        commissionCRUD.grid(row=6, column=1)
        addCom.grid(padx=5, row=6, column=2)
        deleteCom.grid(padx=5, row=6, column=3)
        save.grid(row=7, pady=20)
        close.grid(row=7, column=2, pady=20)

        if HOSP_ORI != None:
            print("hospId:", hosp.id)
            delete = Button(window, text="Delete", command=deleteCallback)
            delete.grid(row=7, column=1, pady=20)
            self.nameVar.set(self.tree.item(self.tree.focus())["values"][1])
            self.codeVar.set(
                self.tree.item(self.tree.focus())["values"][0].replace("\n", "")
            )
        else:
            self.codeVar.set(self.classesManager.classes[0])
            self.nameVar.set(self.classesManager.teachers[0])

        name.bind("<<ComboboxSelected>>", classesForTeacherCallback)
        classesForTeacherCallback(None)
        updateCommissionLabel()

    def createForTeacher(self):
        self.clearWindow()
        self.createSchedule()
        self.createCloseButton()
        hospitations = self.classesManager.getHospsForSchedule(
            self.currentSchedule()
        )
        self.fillTreeWithHosps(hospitations)

    def createForDziekan(self):
        self.createForTeacher()
        self.createEditAddButtons()

