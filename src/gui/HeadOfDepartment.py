from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
import menu
import main.logic.operations
from PIL import ImageTk, Image

teacherId = 4

class TeacherGui():
    def __init__(self, view, cmanager):
        self.classesManager = cmanager
        self.window = view
        self.window.configure(bg="bisque")
        self.window.title("Easy Inspection")
        self.window.geometry("850x500+380+270")
        self.teachersFrame = Frame(self.window, bg='bisque')
        self.chosen = 0

    def clear_frame(self):
        for widgets in self.teachersFrame.winfo_children():
            widgets.destroy()

    def clear_window(self):
        for widgets in self.window.winfo_children():
            if (widgets.winfo_class() != "Frame"):
                widgets.destroy()

    def nextGui(self, fun, tree):
        if (tree.focus()):
            if (fun == self.createHospitationsListGui):
                self.chosen = tree.item(tree.focus())["values"][0]
            fun(tree.item(tree.focus())["values"][0])
        else:
            messagebox.showinfo("Błąd", "Wybierz element")

    def createTeachersListGui(self):
        self.clear_window()
        self.clear_frame()
        self.teachersFrame.place(relx=0.15, rely=0.3)
        teacher = self.classesManager.getTeacher(teacherId)
        Label(self.window, text="Hospitacje nauczycieli katedry: " + teacher.cathedral, bg='bisque', font=48).place(x=170, y=70)
        scrollbar = Scrollbar(self.teachersFrame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        tree = Treeview(self.teachersFrame, column=("c1", "c2", "c3", "c4", "c5"), show='headings', selectmode='browse')
        tree["columns"] = ("1", "2", "3", "4", "5")
        tree.column("1", width=50)
        tree.column("2", width=150)
        tree.column("3", width=150)
        tree.column("5", width=150)
        tree.heading("1", text="Id")
        tree.heading("2", text="Tytuł")
        tree.heading("3", text="Imię")
        tree.heading("4", text="Nazwisko")
        tree.heading("5", text="Liczba hospitacji")
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        teachers = self.classesManager.getCathedralTeachers(teacherId)
        if teachers:
            for teacher in teachers:
                tree.insert("", "end", text="i", values=(
                    str(teacher.id),
                    str(teacher.degree),
                    str(teacher.name),
                    str(teacher.surname),
                    str(main.logic.operations.getHospNum(teacher.id, self.classesManager.hospitations))
                ))
        tree.pack()

        Button(self.window, text='Wróć', height=1, width=10, \
               command=lambda: [self.startGui()]).place(x=570, y=400)
        Button(self.window, text='Wybierz', height=1, width=10, \
                command=lambda: [self.nextGui(self.createHospitationsListGui, tree)]).place(x=170, y=400)
        self.teachersFrame.place(relx=0.1, rely=0.25)
        mainloop()

    def createHospitationsListGui(self, elem):
        self.clear_frame()
        self.clear_window()
        self.teachersFrame.place(relx=0.25, rely=0.3)
        scrollbar = Scrollbar(self.teachersFrame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        tree = Treeview(self.teachersFrame, column=("c1", "c2", "c3", "c4"), show='headings', selectmode='browse', height=10)
        tree["columns"] = ("1", "2", "3", "4")
        tree.heading("1", text="ID")
        tree.heading("2", text="Data")
        tree.heading("3", text="Kurs")
        tree.heading("4", text="Ocena")
        tree.column("1", width=50)
        tree.column("2", width=90)
        tree.column("4", width=80)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        hospitations = self.classesManager.getTeacherHosp(elem)

        if hospitations:
            for hosp in hospitations:
                tree.insert("","end", text = "i", values = (
                    str(hosp.id),
                    str(hosp.date),
                    str(hosp.clas.name),
                    str(main.logic.operations.getMark(hosp.id, self.classesManager.protocols))
                ))

        Label(self.window, text="Hospitacje nauczyciela:    " + str(hospitations[0].teacher.getFullName()),
                        bg='bisque', font=48).place(x=200, y=80)
        tree.pack()

        Button(self.window, text='Wróć', height=1, width=10, \
               command=lambda: [self.clear_frame(), self.createTeachersListGui()]).place(x=570, y=400)
        Button(self.window, text='Wybierz', height=1, width=10, \
               command=lambda: [self.nextGui(self.createProtocolView, tree)]).place(x=170, y=400)

        mainloop()

    def createProtocolView(self, elem):
        protocols = self.classesManager.getHospProtocol(elem)
        mark = main.logic.operations.getMark(elem, self.classesManager.protocols)
        if (protocols):
            self.clear_window()
            self.clear_frame()
            self.teachersFrame.pack(fill='both', expand=True)
            Label(self.teachersFrame, text = "Prowadzący zajęcia:     " + str(protocols.hospitation.teacher.getFullName()),
                                                        bg='bisque').place(x=40, y=20)
            Label(self.teachersFrame, text = "Nazwa zajęć:     " + str(protocols.hospitation.clas.name),
                                                        bg='bisque').place(x=40, y=40)
            Label(self.teachersFrame, text = "Stopień i forma studiów:    " + str(protocols.hospitation.clas.form),
                                                        bg='bisque').place(x=40, y=60)
            Label(self.teachersFrame, text = "Kod kursu:     " + str(protocols.hospitation.clas.code),
                                                        bg='bisque').place(x=40, y=80)
            Label(self.teachersFrame, text = "Semestr:     " + str(protocols.hospitation.schedule.semester.id),
                                                        bg='bisque').place(x=40, y=100)
            Label(self.teachersFrame, text = "Miejsce i termin:     " + str(protocols.hospitation.clas.building) + ", " +
                    str(protocols.hospitation.clas.room) + ", " + str(protocols.hospitation.clas.time), bg='bisque').place(x=40, y=120)
            Label(self.teachersFrame, text = "Hospitujący: ", bg='bisque').place(x=500, y=30)
            Label(self.teachersFrame, text="Wrocław, " + str(protocols.date), bg='bisque').place(x=590, y=5)
            y = 30
            for prot in protocols.hospitation.commission:
                Label(self.teachersFrame, text=str(prot.getFullName()), bg='bisque').place(x=590, y=y)
                y += 20

            scrollbar = Scrollbar(self.teachersFrame)
            scrollbar.pack(side=RIGHT, fill=Y)
            tree = Treeview(self.teachersFrame, column=("c1", "c2"), show='headings', selectmode='browse', height=9)
            tree["columns"] = ("1", "2")
            tree.column("1", width=450)
            tree.column("2", width=80)
            tree.heading("1", text="")
            tree.heading("2", text="")
            tree.configure(xscrollcommand=scrollbar.set)
            tree.insert("", "end", text="i", values=("Przedstawił temat, cel i zakres zajęć", str(protocols.rating[0])))
            tree.insert("", "end", text="i", values=("Wyjaśniał w zrozumiały sposób zagadnienia", str(protocols.rating[1])))
            tree.insert("", "end", text="i", values=("Realizował zajęcia z zaangażowaniem", str(protocols.rating[2])))
            tree.insert("", "end", text="i", values=("Inspirował studentów do samodzielnego myślenia", str(protocols.rating[3])))
            tree.insert("", "end", text="i", values=("Udzielał merytorycznie poprawnych odpwoedzi na pytania studentów",
                                                     str(protocols.rating[4])))
            tree.insert("", "end", text="i", values=("Stosował środki dydaktyczne", str(protocols.rating[5])))
            tree.insert("", "end", text="i", values=("Posługiwał się poprawnym językiem", str(protocols.rating[6])))
            tree.insert("", "end", text="i", values=("Panował nad dynamiką grupy", str(protocols.rating[7])))
            tree.insert("", "end", text="i", values=("Tworzył pozytywną atmosferę na zajęciach", str(protocols.rating[8])))
            tree.place(x=150, y=150)
            Label(self.teachersFrame, text="Ocena końcowa, " + str(mark), bg='bisque').place(x=360, y=370)
            Button(self.window, text='Wróć', height=1, width=10, \
                   command=lambda: [self.createHospitationsListGui(self.chosen)]).place(x=570, y=430)
        else:
            messagebox.showinfo("Błąd", "Protokoły nie zostały jeszcze uzupełnione")

        mainloop()

    def logout(self):
        gui = menu.Menu_GUI()
        gui.start_with_opened_window(self.window, self.classesManager)
        gui.main_window()

    def startGui(self):
        self.clear_window()
        self.clear_frame()
        path = "pwrlogo.png"
        image = Image.open(path)
        zoom = 0.5
        pixels_x, pixels_y = tuple([int(zoom * x) for x in image.size])
        img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
        Label(self.window, image=img).place(x=80, y=30)
        teacher = self.classesManager.getTeacher(teacherId)
        Label(self.window, text="Zalogowany jako: " + teacher.getFullName(), bg='bisque', font=48).place(x=350, y=70)
        Button(self.window, text='Przeglądaj hospitacje nauczycieli', height=1, width=60, \
               command=lambda: [self.createTeachersListGui()]).place(x=220, y=270)
        Button(self.window, text='Wyloguj', height=1, width=20, \
               command=lambda: [self.clear_window(), self.logout()]).place(x=350, y=400)
        mainloop()
