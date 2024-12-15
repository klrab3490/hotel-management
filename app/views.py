import tkinter as tk

class TkiderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Tkider Hotel Management")

        tk.Label(master, text="Available Rooms:").pack()

        self.rooms_listbox = tk.Listbox(master)
        self.rooms_listbox.pack()

        tk.Button(master, text="Load Rooms").pack()


