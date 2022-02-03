from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Combobox
import HospitationsSchedule, menu
from PIL import ImageTk, Image

teacherId = 27
class InspectorGui():
    def __init__(self, view, cmanager):
        self.classesManager = cmanager
        self.window = view
        self.window.configure(bg="bisque")
        self.window.title("Easy Inspection")
        self.window.geometry("850x500+380+270")
        self.teachersFrame = Frame(self.window, bg='bisque')

    def clearFrame(self):
        for widgets in self.teachersFrame.winfo_children():
            widgets.destroy()

    def clearWindow(self):
        for widgets in self.window.winfo_children():
            if (widgets.winfo_class() != "Frame"):
                widgets.destroy()

    def nextGui(self, fun, tree):
        if (tree.focus()):
            fun(tree.item(tree.focus())["values"][0])
        else:
            messagebox.showinfo("Błąd", "Wybierz element")

    def createProtocolsGui(self):
        scrollbar = Scrollbar(self.teachersFrame, orient=VERTICAL)
        self.clearWindow()
        scrollbar.pack(side=RIGHT, fill=Y)
        tree = Treeview(self.teachersFrame, column=("c1", "c2", "c3", "c4"), show='headings', selectmode='browse')
        tree["columns"] = ("1", "2", "3", "4")
        tree.column("1", width=50)
        tree.column("2", width=100)
        tree.column("3", width=200)
        tree.column("4", width=150)
        tree.heading("1", text="ID")
        tree.heading("2", text="Data")
        tree.heading("3", text="Hospitowany")
        tree.heading("4", text="Nazwa kursu")
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        hospitations = self.classesManager.getTeacherProtocolsToMake(teacherId)
        if hospitations:
            for hosp in hospitations:
                tree.insert("","end", text="i", values=(
                    str(hosp.id),
                    str(hosp.date),
                    str(hosp.teacher.getFullName()),
                    str(hosp.clas.name)
                ))
        else:
            messagebox.showinfo("Informacja", "Brak protokołów wymagających uzupełnienia")
        tree.pack()
        Label(self.window, text="Protokoły wymagające uzupełnienia: ", bg='bisque', font=48).place(x=270, y=40)
        Button(self.window, text='Wróć', height=1, width=10, command=lambda: [self.startGui()]).place(x=570, y=400)
        Button(self.window, text='Wybierz', height=1, width=10,
               command=lambda: [self.nextGui(self.createProtocolView, tree)]).place(x=170, y=400)
        self.teachersFrame.place(relx=0.2, rely=0.2)
        mainloop()

    def createProtocolView(self, elem):
        hospitation = self.classesManager.getHospData(elem)
        if (hospitation):
            self.clearWindow()
            self.clearFrame()
            self.teachersFrame.pack(fill='both', expand=True)
            Label(self.teachersFrame,
                  text="Prowadzący zajęcia:     " + str(hospitation.teacher.getFullName()),
                      bg='bisque').place(x=40, y=20)
            Label(self.teachersFrame, text="Nazwa zajęć:     " + str(hospitation.clas.name),
                      bg='bisque').place(x=40, y=40)
            Label(self.teachersFrame, text="Stopień i forma studiów:    " + str(hospitation.clas.form),
                      bg='bisque').place(x=40, y=60)
            Label(self.teachersFrame, text="Kod kursu:     " + str(hospitation.clas.code),
                      bg='bisque').place(x=40, y=80)
            Label(self.teachersFrame, text="Semestr:     " + str(hospitation.schedule.semester.id),
                      bg='bisque').place(x=40, y=100)
            Label(self.teachersFrame,
                      text="Miejsce i termin:     " + str(hospitation.clas.building) + ", " +
                           str(hospitation.clas.room) + ", " + str(hospitation.clas.time),
                      bg='bisque').place(x=40, y=120)
            Label(self.teachersFrame, text="Hospitujący: ", bg='bisque').place(x=500, y=30)
            Label(self.teachersFrame, text="Wrocław, " + str(hospitation.date), bg='bisque').place(x=590, y=5)
            y = 30

            for prot in hospitation.commission:
                Label(self.teachersFrame, text=str(prot.getFullName()), bg='bisque').place(x=590, y=y)
                y += 20

            Label(self.teachersFrame, text=("Przedstawił temat, cel i zakres zajęć"), bg='bisque').place(x=100, y=170)
            Label(self.teachersFrame, text=("Wyjaśniał w zrozumiały sposób zagadnienia"), bg='bisque').place(x=100, y=200)
            Label(self.teachersFrame, text=("Realizował zajęcia z zaangażowaniem"), bg='bisque').place(x=100, y=230)
            Label(self.teachersFrame, text=("Inspirował studentów do samodzielnego myślenia"), bg='bisque').place(x=100, y=260)
            Label(self.teachersFrame, text=("Udzielał merytorycznie poprawnych odpwoedzi na pytania studentów"), bg='bisque').place(x=100, y=290)
            Label(self.teachersFrame, text=("Stosował środki dydaktyczne"), bg='bisque').place(x=100, y=320)
            Label(self.teachersFrame, text=("Posługiwał się poprawnym językiem"), bg='bisque').place(x=100, y=350)
            Label(self.teachersFrame, text=("Panował nad dynamiką grupy"), bg='bisque').place(x=100, y=380)
            Label(self.teachersFrame, text=("Tworzył pozytywną atmosferę na zajęciach"), bg='bisque').place(x=100, y=410)

            combos = {}
            y = 170
            for x in range(1, 10):
                combos["string{0}".format(x)] = Combobox(self.teachersFrame, width=11)
                combos["string{0}".format(x)].place(x=550, y=y)
                combos["string{0}".format(x)]['values'] = ('Nie dotyczy', '3', '3.5', '4', '4.5', '5', '5.5')
                y += 30

            def insert(hospitation, boxes):
                inserted = self.classesManager.insertProtocol(hospitation, boxes)
                if(not inserted):
                   messagebox.showinfo(self.teachersFrame, "Wprowadź wartość")
                else:
                    messagebox.showinfo("Inforamcja", "Zapisano do bazy")
                    self.createProtocolsGui()

            Button(self.window, text='Zapisz', height=1, width=10,
                   command=lambda: [insert(hospitation, combos)]).place(x=200, y=450)
            Button(self.window, text='Wróć', height=1, width=10,
                       command=lambda: [self.createProtocolsGui()]).place(x=570, y=450)
        else:
            messagebox.showinfo("Błąd", "Protokół nie został jeszcze uzupełniony")

        mainloop()

    def logout(self):
        gui = menu.Menu_GUI()
        gui.start_with_opened_window(self.window, self.classesManager)
        gui.main_window()

    def lookSchedule(self):
        scheduleGui = HospitationsSchedule.ScheduleGui(self.window, self.classesManager)
        scheduleGui.createForTeacher()

    def startGui(self):
        self.clearWindow()
        self.clearFrame()
        path = "pwrlogo.png"
        image = Image.open(path)
        zoom = 0.5
        pixels_x, pixels_y = tuple([int(zoom * x) for x in image.size])
        img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
        Label(self.window, image=img).place(x=80, y=30)
        teacher = self.classesManager.getTeacher(teacherId)
        Label(self.window, text="Zalogowany jako: " + teacher.getFullName(), bg='bisque', font=48).place(x=290, y=70)
        Button(self.window, text='Uzupełnij protokoły', height=1, width=60,
               command=lambda: [self.createProtocolsGui()]).place(x=210, y=200)
        Button(self.window, text='Zapoznaj się z Kartami Przedmiotów', height=1, width=60,
               command=lambda: [messagebox.showinfo("Info", "W następneym wydaniu")]).place(x=210, y=250)
        Button(self.window, text='Przejrzyj harmonogram hospitacji', height=1, width=60,
               command=lambda: [self.lookSchedule()]).place(x=210, y=300)
        Button(self.window, text='Wyloguj', height=1, width=20,
               command=lambda: [self.clearWindow(), self.logout()]).place(x=350, y=400)
        mainloop()
