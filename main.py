from tkinter import *
from tkinter import messagebox
from db import session, login

# Tkinter GUI Setup
app = Tk()
app.title("Hotel Management")
app.geometry("1500x800")

user_Name = StringVar()


"""Login"""
class Login:
    def __init__(self, master):
        self.master = master
        self.window = Toplevel(self.master)
        self.window.title("Login")
        self.window.geometry("300x200")
        
        # Ensure the login window stays on top of the main window
        self.window.transient(self.master)
        self.window.grab_set()

        # Title label
        Label(self.window, text="Login", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Username label and entry
        Label(self.window, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.username_entry = Entry(self.window, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        # Password label and entry
        Label(self.window, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.password_entry = Entry(self.window, font=("Arial", 12), show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Login button
        Button(self.window, text="Login", font=("Arial", 12), command=self.handle_login).grid(row=3, column=0, columnspan=2, pady=20)

        # Optionally, add a status label for errors or success messages
        self.status_label = Label(self.window, text="", font=("Arial", 10), fg="red")
        self.status_label.grid(row=4, column=0, columnspan=2)

    """Handles the login process."""
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Attempt login
        success, message = login(username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.window.destroy()  # Close the login window
            if session['role'] == 'admin':
                show_main_admin()
            else:
                show_main_user()
        else:
            messagebox.showerror("Error", message)


def show_main_admin():
    global app, session
    # If there's no logged-in user, show an error message
    if 'user' not in session:
        messagebox.showerror("Error", "No user logged in.")
        app.destroy()
        return

    # Get user data from session
    user_Name.set(session.get('name', 'Unknown User'))

    # Your main application UI setup
    Label(app, text="Welcome to Hotel Management", font=("Arial", 24)).pack(pady=20)
    Label(app, text="Admin", font=("Arial", 24)).pack(pady=20)
    Label(app, textvariable=user_Name, font=("Arial", 24)).pack(pady=20)

    mymenu = Menu(app)
    app.config(menu=mymenu)
    file = Menu(mymenu)
    mymenu.add_cascade(label="File",menu=file)
    file.add_command(label="New")
    file.add_separator()
    file.add_command(label="Exit", command=app.quit)


def show_main_user():
    global app, session
    # If there's no logged-in user, show an error message
    if 'user' not in session:
        messagebox.showerror("Error", "No user logged in.")
        app.destroy()
        return

    # Get user data from session
    user_Name.set(session.get('name', 'Unknown User'))

    # Your main application UI setup
    Label(app, text="Welcome to Hotel Management", font=("Arial", 24)).pack(pady=20)
    Label(app, text="User", font=("Arial", 24)).pack(pady=20)
    Label(app, textvariable=user_Name, font=("Arial", 24)).pack(pady=20)

    mymenu = Menu(app)
    app.config(menu=mymenu)
    file = Menu(mymenu)
    mymenu.add_cascade(label="File",menu=file)
    file.add_command(label="New")
    file.add_separator()
    file.add_command(label="Exit", command=app.quit)

"""Check if the user is logged in or not."""
def check_login():
    if 'user' in session:
        # If logged in, show the main app window
        if session['role'] == 'admin':
            show_main_admin()
        else:
            show_main_user()
    else:
        # If not logged in, show the login window
        Login(app)  


# Start by checking login status
check_login()

# Start the Tkinter main loop
app.mainloop()
