from tkinter import *
from tkinter.ttk import Style
import main.classes.ClassesManager
import InspectedTeacher, HeadOfDepartment, Inspector, HospitationsSchedule


class Menu_GUI():
    def __init__(self):
        pass
        # messagebox.showinfo("Database", result["data"])


    def start(self):
        self.classesManager = main.classes.ClassesManager.ClassesManager()
        result = self.classesManager.connectToDb()
        self.classesManager.pullFromDatabase()
        self.root = Tk()
        self.root.withdraw()
        self.window = Toplevel(self.root)
        self.window.title("Easy Inspection")
        self.window.geometry("850x500+380+270")
        self.window.configure(bg="bisque")
        self.style = Style()
        self.style.theme_use("classic")
        #self.style.configure("Treeview", rowheight=80)

    def start_with_opened_window(self, view, cmanager):
        self.classesManager = cmanager
        self.window = view
        self.window.title("Easy Inspection")
        self.window.geometry("850x500+380+270")
        self.window.configure(bg="bisque")
        self.style = Style()
        self.style.theme_use("classic")
        #self.style.configure("Treeview", rowheight=80)

    def clear_frame(self):
        for widgets in self.window.winfo_children():
            widgets.destroy()

    def main_window(self):
        self.intro()
        mainloop()

    def intro(self):
        label1 = Label(self.window, text="Easy Inspection", bg="bisque", font="76")
        label1.pack(pady=20)

        self.entry = Entry(self.window,  width=10)
        self.entry.pack(pady=10)

        but = Button(self.window, text="Hospitowani", command=lambda: [ label1.destroy(),but.destroy(), but2.destroy(),but3.destroy(),but4.destroy(),
                                                                        self.chosen_menu_stasiu(self.entry.get())], width=20)
        but2 = Button(self.window, text="Hospitujący", command=lambda: [self.clear_frame(), self.chosen_menu_oscik2()], width=20)
        but3 = Button(self.window, text="Dziekan", command=lambda: [self.clear_frame(), self.chosen_menu_pawel()], width=20)
        but4 = Button(self.window, text="Kierownik katedry", command=lambda: [self.clear_frame(), self.chosen_menu_oscik()], width=20)

        but.pack(pady=10)
        but2.pack(pady=10)
        but3.pack(pady=10)
        but4.pack(pady=10)

        def closeDb():
            self.classesManager.closeConnection()

        but4 = Button(self.window, text="Wyjdź", command=lambda: [self.window.destroy(), closeDb(), exit()])
        but4.pack()

    def chosen_menu_oscik(self):
        headOfDep = HeadOfDepartment.TeacherGui(self.window, self.classesManager)
        headOfDep.startGui()

    def chosen_menu_oscik2(self):
        inspector = Inspector.InspectorGui(self.window, self.classesManager)
        inspector.startGui()

    def chosen_menu_pawel(self):
        pawelGui = HospitationsSchedule.ScheduleGui(self.window, self.classesManager)
        pawelGui.createForDziekan()

    def chosen_menu_stasiu(self, id):
        self.entry.destroy()
        if(id != ""):
            gui = InspectedTeacher.HistoryGui(self.window, self.classesManager, int(id))
            gui.main_window()
        else:
            self.intro()

if __name__ == "__main__":
    gui = Menu_GUI()
    gui.start()
    gui.main_window()