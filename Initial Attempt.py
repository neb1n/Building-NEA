from tkinter import *
from tkinter import ttk

global Jack
Jack = False #login variable initalised to be false everytime we start the program

class app:
    def __init__(self, master):  # defines the master function
        self.master = master
        self.menu()

    def menu(self):
        for widget in self.master.winfo_children():  # destroys previous frames
            widget.destroy()

        self.frame1 = Frame(self.master, width=70, height=200)
        self.frame1.pack()
        self.reg_txt = ttk.Label(self.frame1, text='Main', width=150).pack()
        self.gtlogin_btn = ttk.Button(self.frame1, text = "Go to login", command = self.login, width = 30).pack()
        self.edit_btn = ttk.Button(self.frame1, text="Go to edit", command=self.edit, width=30).pack()
        self.read_btn = ttk.Button(self.frame1, text="Go to read", command=self.read, width=30).pack()

    def edit(self):
        if Jack == True:
            for widget in self.master.winfo_children():
                widget.destroy()

            self.frame2 = Frame(self.master, width=300, height=700)
            self.frame2.pack()

            self.reg_txt2 = ttk.Label(self.frame2, text='Edit').pack()
            self.name_lbl = ttk.Label(self.frame2, text='Name').pack()
            self.name_txt = Text(self.frame2, width=20, height=3)
            self.name_txt.pack()

            self.dire_lbl = ttk.Label(self.frame2, text='Director').pack()
            self.dire_txt = Text(self.frame2, width=20, height=3)
            self.dire_txt.pack()

            self.load_btn = ttk.Button(self.frame2, text="Load", width=20, command=self.load).pack()
            self.save_btn = ttk.Button(self.frame2, text="Save", width=20, command=self.save).pack()
            self.replace_btn = ttk.Button(self.frame2, text="Replace", width=20, command=self.replace).pack()
            self.main_btn = ttk.Button(self.frame2, text="Go to menu", command=self.menu).pack()
        else:
            top = Toplevel(root)
            top.geometry("200x100")
            top.title("LOGIN")
            Label(top, text = "Please login first", font =("Arial 12 bold")).pack()
            Button(top, text = "OK", font = ("Arial 12 bold"), command = self.login).pack()

    def read(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.frame3 = Frame(self.master, width=300, height=700)
        self.frame3.pack()
        self.reg_txt3 = ttk.Label(self.frame3, text='Read').pack()
        self.main_btn = ttk.Button(self.frame3, text="Go to menu", command=self.menu).pack()

    def login(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.frame4 = Frame(self.master, width = 300, height = 700)
        self.frame4.pack()
        self.login_lbl = ttk.Label(self.frame4, text = "Login").pack()
        self.username_lbl = ttk.Label(self.frame4, text = "Username").pack()
        self.username_txt = Text(self.frame4, width = 20, height = 3)  # Consider using Entry for username
        self.username_txt.pack()
        self.password_lbl = ttk.Label(self.frame4, text = "Password").pack()
        self.password_txt = Text(self.frame4, width = 20, height = 3)  # Consider using Entry for password
        self.password_txt.pack()
        self.login_btn = ttk.Button(self.frame4, text = "Login", command = self.atmptlogin).pack()

    def replace(self):
        changename = self.name_txt.get("1.0", "end-1c").strip()
        changedirector = self.dire_txt.get("1.0", "end-1c").strip()
        old = {}

        # Read the file into a dictionary
        with open("movies.txt", "r") as f:
            oldlines = f.readlines()
            for line in oldlines:
                oldname, oldirector = line.strip().split(":")
                old[oldname.strip()] = oldirector.strip()

        # If movie exists, replace its director
        if changename in old:
            old[changename] = changedirector
            with open("movies.txt", "w") as f:
                for name, director in old.items():
                    f.write(f"{name}: {director}\n")
            print("Movie replaced")
        else:
            print(f"Movie '{changename}' not found, saving new entry.")
            self.save()

    def save(self):
        name = self.name_txt.get("1.0", "end-1c").strip()
        director = self.dire_txt.get("1.0", "end-1c").strip()

        if name and director:
            with open("movies.txt", "a") as f:
                f.write(f"{name}: {director}\n")
            print("Movie saved")
        else:
            print("Name or Director cannot be empty!")

    def load(self):
        name = self.name_txt.get("1.0", "end-1c").strip()
        joint = {}

        with open("movies.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                movie_name, director = line.strip().split(":")
                joint[movie_name.strip()] = director.strip()

        if name in joint:
            director = joint[name]
            self.dire_txt.delete("1.0", END)
            self.dire_txt.insert("1.0", director)
        else:
            self.dire_txt.delete("1.0", END)
            self.dire_txt.insert("1.0", "Cannot find movie")

    def atmptlogin(self):
        global Jack  # Ensure you're modifying the global variable
        username = self.username_txt.get("1.0", "end-1c")
        password = self.password_txt.get("1.0", "end-1c")
        
        if username == "Admin" and password == "Admin1":
            print("Logged in")
            Jack = True  # Set global Jack to True
            self.menu()  # After successful login, go back to the menu
        else:
            print("Incorrect try again")
            Jack = False  # Set global Jack to False

root = Tk()
root.title("Movie Management")
app(root)
root.mainloop()
