import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import glob

# Prototype Build for the NEA Version: 1.07 14/03/25
# Most recent change: Changed the JACK to no longer be global but instead changed into the class so that it's no longer global.
# Current thoughts: I need to add the next part which is probably the edit/adding to the file page.
# Current Song: Aasa Kooda - Sai Abhyankar

class App:
    def __init__(self, master):  # defines the master function
        self.master = master
        self.Jack = False  # not logged in
        self.menu()  # Show the menu initially

    # All the pages
    def menu(self):
        for widget in self.master.winfo_children():  # destroys previous frames
            widget.destroy()

        self.menuframe = Frame(self.master, width=70, height=200, padx=10, pady=10)
        self.menuframe.pack(padx=20, pady=20)

        self.reg_txt = ttk.Label(self.menuframe, text='Main', width=150).pack()

        self.gtlogin_btn = ttk.Button(self.menuframe, text="Go to login", command=self.login, width=30).pack()
        self.edit_btn = ttk.Button(self.menuframe, text="Go to edit", command=self.edit, width=30).pack()
        self.bookings_btn = ttk.Button(self.menuframe, text="Go to bookings", command=self.book, width=30).pack()

    def edit(self):
        if self.Jack:  # check if the user is logged in
            for widget in self.master.winfo_children():
                widget.destroy()

            self.editframe = Frame(self.master, width=300, height=700)
            self.editframe.pack()

            self.editlbl = ttk.Label(self.editframe, text='Edit').pack()
            self.name_lbl = ttk.Label(self.editframe, text='Name').pack()
            self.name_txt = Text(self.editframe, width=20, height=3)
            self.name_txt.pack()

            self.dire_lbl = ttk.Label(self.editframe, text='Director').pack()
            self.dire_txt = Text(self.editframe, width=20, height=3)
            self.dire_txt.pack()

            self.load_btn = ttk.Button(self.editframe, text="Load", width=20).pack()
            self.save_btn = ttk.Button(self.editframe, text="Save", width=20).pack()
            self.replace_btn = ttk.Button(self.editframe, text="Replace", width=20).pack()
            self.main_btn = ttk.Button(self.editframe, text="Go to menu", command=self.menu).pack()
        else:
            top = Toplevel(self.master)
            top.geometry("200x100")
            top.title("Login")
            Label(top, text="Please login first", font=("Arial 12 bold")).pack()
            Button(top, text="Send to login", font=("Arial 12 bold"), command=self.login).pack()
            Button(top, text="Exit", font=("Arial 12 bold"), command=self.menu).pack()

    def book(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.bookframe = Frame(self.master, width=300, height=700)
        self.bookframe.pack()
        self.bookingslbl = ttk.Label(self.bookframe, text='Bookings').pack()

        # getting the image carousel ready
        self.image_list = self.load_images()
        self.current_image_index = 0

        # displaying the image on the label
        self.image_label = Label(self.bookframe)
        self.image_label.pack()

        # carousel begins
        self.show_image()

        # make it so that when the image is clicked, the file name appears
        self.image_label.bind("<Button-1>", self.on_image_click)

        # going backwards and forwards in the button
        self.prev_btn = ttk.Button(self.bookframe, text="Previous", command=self.prev_image).pack()
        self.next_btn = ttk.Button(self.bookframe, text="Next", command=self.next_image).pack()

        # the text part where I display the movie name
        self.moviename = Text(self.bookframe, width=20, height=3)
        self.moviename.pack()

        self.main_btn = ttk.Button(self.bookframe, text="Go to menu", command=self.menu).pack()

    def login(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.loginframe = Frame(self.master, width=300, height=700)
        self.loginframe.pack()

        self.login_lbl = ttk.Label(self.loginframe, text="Login").pack()
        self.username_lbl = ttk.Label(self.loginframe, text="Username").pack()
        self.username_txt = Entry(self.loginframe, width=20)  # changed to Entry widget
        self.username_txt.pack()

        self.password_lbl = ttk.Label(self.loginframe, text="Password").pack()
        self.password_txt = Entry(self.loginframe, width=20, show="*")  # changed to Entry widget with a hidden password
        self.password_txt.pack()

        self.login_btn = ttk.Button(self.loginframe, text="Login", command=self.atmptlogin).pack()
        self.home_btn = ttk.Button(self.loginframe, text="Menu", command=self.menu).pack()

    # All the methods
    def on_image_click(self, event):
        # when the image is clicked
        image_path = self.image_list[self.current_image_index]
        filename_without_extension = os.path.splitext(os.path.basename(image_path))[0]

        # updating the text box
        self.moviename.delete("1.0", "end")
        self.moviename.insert("1.0", filename_without_extension)  # add the filename without the extension

    def load_images(self):
        # make sure to change the path
        images_path = glob.glob("images/*.jpg") 
        return images_path

    def show_image(self):
        # loading the image based on the index (had to google this part)
        image_path = self.image_list[self.current_image_index]
        image = Image.open(image_path)
        image = image.resize((300, 200))  # resizing the image
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # i don't know what this does but i think i needed it 

        # it does this after so that like there's some delay
        

    def save_movie(self):
        movie_name = self.name_txt.get("1.0", "end-1c").strip()
        director_name = self.dire_txt.get("1.0", "end-1c").strip()

        if movie_name and director_name:
            with open("movies.txt", "a") as f:
                f.write(f"{movie_name}:{director_name}\n")
            print("Movie saved")
        else:
            print("Name or director cannot be empty")

    def next_image(self):
        # next image
        self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
        self.show_image()

    def prev_image(self):
        # previous image
        self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
        self.show_image()

    def atmptlogin(self):
        username = self.username_txt.get("1.0", "end-1c")
        password = self.password_txt.get("1.0", "end-1c")

        if username == "Admin" and password == "Admin1":
            print("Logged in")
            self.Jack = True  # logged in
            self.menu()  # sends you back to the menu
        else:
            print("Incorrect, try again")
            self.Jack = False  # not logged in

main = Tk()
main.title("Movie Management")  
app(main)
main.mainloop()
