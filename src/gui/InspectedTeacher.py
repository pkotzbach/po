from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from PIL import ImageTk, Image
import menu as m
import main.logic.operations


# chosen_person_id = 18 #z protokolami
# chosen_person_id = 2 #bez

class HistoryGui():
    def __init__(self,view, cmanager, id=18):
        self.classesManager = cmanager
        self.chosen_person_id = id
        self.window = view
        self.window.configure(bg="bisque")


    def clear_frame(self):
        for widgets in self.historyFrame.winfo_children():
            widgets.destroy()

    def clear_window(self):
        for widgets in self.window.winfo_children():
            widgets.destroy()

    def main_window(self):
        self.intro()
        mainloop()

    def to_menu(self):
        gui = m.Menu_GUI()
        gui.start_with_opened_window(self.window, self.classesManager)
        gui.main_window()

    def intro(self):
        self.clear_window()
        path = "pwrlogo.png"
        image = Image.open(path)
        zoom = 0.5
        pixels_x, pixels_y = tuple([int(zoom * x) for x in image.size])
        img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
        Label(self.window, image=img).place(x=80, y=30)
        label1 = Label(self.window, text="Easy Inspection", bg="bisque", font="76")
        label2 = Label(self.window, text="Historia Hospitacji:", bg="bisque")
        but = Button(self.window, text="Przejdź", command=lambda: [self.create_hospitation_list()])
        but2 = Button(self.window, text="Wyloguj", command=lambda: [self.clear_window(), self.to_menu()])

        label1.place(relx=0.4, rely=0.2)
        label2.place(relx=0.3, rely=0.4)
        but.place(relx=0.55, rely=0.4)
        but2.place(relx=0.45, rely=0.6)


    def create_hospitation_list(self):
        self.clear_window()
        self.historyFrame = Frame(self.window)
        scrollbar = Scrollbar(self.historyFrame, orient= VERTICAL)

        tree = Treeview(self.historyFrame, column=("c1", "c2", "c3", "c4"), show='headings', selectmode='browse')
        tree["columns"] = ("1", "2", "3", "4")
        tree.heading("1", text="ID")
        tree.heading("2", text="Data")
        tree.heading("3", text="Kurs")
        tree.heading("4", text="Ocena")
        tree.column("1", width=50)
        tree.column("4", width=50)
        tree.configure(xscrollcommand=scrollbar.set)

        hospitations = self.classesManager.getTeacherHosp(self.chosen_person_id)
        if hospitations:
            for hosp in hospitations:
                prot = "nd."
                if(hosp.protocolCreated):
                    prot = main.logic.operations.getMark(hosp.id, self.classesManager.protocols)
                tree.insert("", "end", text="i", values=(
                    str(hosp.id),
                    str(hosp.date),
                    str(hosp.clas.name),
                    prot,
                ))
        else:
            self.intro()
            messagebox.showinfo("Powiadomienie", "Brak przeprowadzonych hospitacji w historii")
            return

        scrollbar.pack(side=RIGHT, fill=Y)
        tree.pack()
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        myLabel = Label(self.window, text="Wybór Hospitacji", bg="bisque", font="48")
        but = Button(self.window, text="Powrót", command=lambda: [self.intro()])
        but2 = Button(self.window, text="Wybierz", command=lambda:[self.createProtocolView(tree.item(tree.focus())["values"][0])])

        myLabel.place(relx=0.4, rely=0.0)
        but.place(relx=0.75, rely=0.8)
        but2.place(relx=0.15, rely=0.8)
        self.historyFrame.place(relx=0.2, rely=0.1)


    def createProtocolView(self, elem):
        protocols = self.classesManager.getHospProtocol(elem)
        if (protocols):
            self.clear_window()
            self.historyFrame = Frame(self.window)
            self.historyFrame.pack(fill='both', expand=True)
            self.historyFrame.configure(bg='bisque')
            teacher = Label(self.historyFrame,
                            text="Prowadzący zajęcia:     " + str(protocols.hospitation.teacher.getFullName()),
                            bg='bisque')
            className = Label(self.historyFrame, text="Nazwa zajęć:     " + str(protocols.hospitation.clas.name),
                              bg='bisque')
            form = Label(self.historyFrame, text="Stopień i forma studiów:    " + str(protocols.hospitation.clas.form),
                         bg='bisque')
            code = Label(self.historyFrame, text="Kod kursu:     " + str(protocols.hospitation.clas.code), bg='bisque')
            sem = Label(self.historyFrame, text="Semestr:     " + str(protocols.hospitation.schedule.semester.id),
                        bg='bisque')
            place = Label(self.historyFrame,
                          text="Miejsce i termin:     " + str(protocols.hospitation.clas.building) + ", " +
                               str(protocols.hospitation.clas.room) + ", " + str(protocols.hospitation.clas.time),
                          bg='bisque')
            commision = Label(self.historyFrame, text="Hospitujący: ", bg='bisque')
            date = Label(self.historyFrame, text="Wrocław, " + str(protocols.date), bg='bisque')

            text = ""
            for prot in protocols.hospitation.commission:
                text += str(prot.getFullName())+ "\n"
            com = Label(self.historyFrame, text=text, bg='bisque')
            com.place(x=590, y=30)

            date.place(x=590, y=5)
            teacher.place(x=40, y=20)
            className.place(x=40, y=40)
            form.place(x=40, y=60)
            code.place(x=40, y=80)
            sem.place(x=40, y=100)
            place.place(x=40, y=120)
            commision.place(x=500, y=30)

            scrollbar = Scrollbar(self.historyFrame)
            scrollbar.pack(side=RIGHT, fill=Y)
            tree = Treeview(self.historyFrame, column=("c1", "c2"), show='headings', selectmode='browse', height=9)
            tree["columns"] = ("1", "2")
            tree.column("1", width=450)
            tree.column("2", width=100)
            tree.heading("1", text="")
            tree.heading("2", text="Ocena")
            tree.configure(xscrollcommand=scrollbar.set)
            tree.insert("", "end", text="i", values=("Przedstawił temat, cel i zakres zajęć", str(protocols.rating[0])))
            tree.insert("", "end", text="i",
                        values=("Wyjaśniał w zrozumiały sposób zagadnienia", str(protocols.rating[1])))
            tree.insert("", "end", text="i", values=("Realizował zajęcia z zaangażowaniem", str(protocols.rating[2])))
            tree.insert("", "end", text="i",
                        values=("Inspirował studentów do samodzielnego myślenia", str(protocols.rating[3])))
            tree.insert("", "end", text="i", values=("Udzielał merytorycznie poprawnych odpwoedzi na pytania studentów",
                                                     str(protocols.rating[4])))
            tree.insert("", "end", text="i", values=("Stosował środki dydaktyczne", str(protocols.rating[5])))
            tree.insert("", "end", text="i", values=("Posługiwał się poprawnym językiem", str(protocols.rating[6])))
            tree.insert("", "end", text="i", values=("Panował nad dynamiką grupy", str(protocols.rating[7])))
            tree.insert("", "end", text="i",
                        values=("Tworzył pozytywną atmosferę na zajęciach", str(protocols.rating[8])))
            tree.place(x=150, y=150)

            but = Button(self.window, text="Powrót",
                         command=lambda: [self.create_hospitation_list()])

            but.place(relx=0.65, rely=0.8)

            mark = main.logic.operations.getMark(elem, self.classesManager.protocols)
            label_mark = Label(self.window, text="Ocena końcowa: " + str(mark), bg='bisque')
            label_mark.place(relx=0.4, rely=0.75)
            but2 = Button(self.window, text="Odwołanie",
                         command=lambda: [self.create_appeal(elem)])

            but2.place(relx=0.15, rely=0.8)
        else:
            myLabel = Label(self.window, text="Wybór Hospitacji", bg="bisque", font="48")
            myLabel.place(relx=0.4, rely=0.0)
            messagebox.showinfo("Powiadomienie", "Nie stworzono protokołu")

    def create_appeal(self,elem):
        self.clear_window()
        protocols = self.classesManager.getHospProtocol(elem)
        title = Label(self.window, text="Odwołanie", font=72, bg='bisque')
        text = Label(self.window, text="Niniejszym odwołuję się od oceny hospitacji " + str(elem) + " z dnia "+  str(protocols.date) + "\n" +
                                       "ponieważ nie zgadzam się z oceną końcową", bg='white', font=48)
        button_send= Button(self.window, text="Prześlij",command=lambda: [self.appeal_sent(protocols)])
        button_back = Button(self.window, text="Powrót", command=lambda: [self.clear_window(), self.createProtocolView(elem)])
        title.place(relx=0.45, rely=0.2)
        text.place(relx=0.15, rely=0.4)
        button_send.place(relx=0.15, rely=0.8)
        button_back.place(relx=0.75, rely=0.8)

    def appeal_sent(self, protocol):
        print(protocol.appeal)
        if(protocol.appeal == False):
            self.classesManager.updateProtocol(protocol.id)
            messagebox.showinfo("Powiadomienie", "Przesłano odwołanie")
            self.clear_window()
            self.intro()

        else:
            messagebox.showinfo("Powiadomienie", "Przesłanie zakończono niepowodzeniem")

if __name__ == "__main__":
    gui = HistoryGui()
    gui.main_window()