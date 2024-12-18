from tkinter import *
from tkinter import messagebox, ttk
from db import session, login, getDB

# Tkinter GUI Setup
app = Tk()
app.title("Hotel Management")
app.geometry("1500x800+0+0")

user_Name = StringVar()
bton_data = ""

class Login:
    def __init__(self, master):
        self.master = master
        self.window = Toplevel(self.master)
        self.window.title("Login")
        self.window.geometry("300x200+150+150")
        
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
        Button(self.window, text="Login", font=("Arial", 12), command=self.handle_login).grid(row=3, column=0, columnspan=2)
        Button(self.window, text="Exit", font=("Arial", 12), command=lambda: master.destroy()).grid(row=4, column=0, columnspan=2)

        # Status label for errors or success messages
        self.status_label = Label(self.window, text="", font=("Arial", 10), fg="red")
        self.status_label.grid(row=4, column=0, columnspan=2)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Attempt login
        success, message = login(username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.window.destroy()  # Close the login window
            check_login()
        else:
            messagebox.showerror("Error", message)
        

class DisplayData:
    def __init__(self, parent, data, collection):
        # Create a new Toplevel window
        self.window = Toplevel(parent)
        self.window.title(f"{collection.capitalize()} Data")
        self.window.geometry("900x400")

        # Define the Treeview widget
        self.tree = ttk.Treeview(self.window)
        
        # Map the columns based on the collection
        collection_map = {
            "guest": ("Guest ID", "Name", "Email", "Phone", "Address", "Room No", "Check In", "Check Out", "Status"),
            "inventory": ("Item Name", "Quantity", "Price"),
            "rooms": ("Room No", "Type", "Status", "Price"),
            "staff": ("Staff ID", "Name", "Role", "Email", "Phone", "Address", "Shift", "Salary", "Status"),
            "user": ("User ID", "Username", "Name", "Role")
        }

        if collection in collection_map:
            columns = collection_map[collection]
            self.tree["columns"] = columns
            self.tree["show"] = "headings"  # Show only headings, not the default empty column

            # Configure column headings
            for col in columns:
                self.tree.heading(col, text=col, anchor="w")
                self.tree.column(col, anchor="w", width=100)  # Adjust column width as needed

            # Insert data into the Treeview
            for item in data:
                if collection == "guest":
                    self.tree.insert("", "end", values=(item['guest_id'], item['name'], item['email'], item['phone'], item['address'], item['room_no'], item['check_in'], item['check_out'], item['status']))
                elif collection == "inventory":
                    self.tree.insert("", "end", values=(item['item'], item['quantity'], item['price']))
                elif collection == "rooms":
                    self.tree.insert("", "end", values=(item['room_no'], item['type'], item['status'], item['price']))
                elif collection == "staff":
                    self.tree.insert("", "end", values=(item['staff_id'], item['name'], item['role'], item['email'], item['phone'], item['address'], item['shift'], item['salary'], item['status']))
                elif collection == "user":
                    self.tree.insert("", "end", values=(item['user_id'], item['username'], item['name'], item['role']))

        # Pack the Treeview widget
        self.tree.pack(expand=True, fill="both")

        # Add a close button
        close_button = ttk.Button(self.window, text="Close", command=self.window.destroy)
        close_button.pack(pady=10)

def show_data(collection):
    global app
    success, data, message = getDB(collection)
    if success:
        DisplayData(app, data, collection)
    else:
        messagebox.showerror("Error", message)

def show_main(role):
    global app, session
    if 'user' not in session:
        messagebox.showerror("Error", "No user logged in.")
        app.quit()
        return

    # Clear any previous widgets from the window
    for widget in app.winfo_children():
        widget.destroy()

    mymenu = Menu(app)
    app.config(menu=mymenu)

    db = Menu(mymenu)
    mymenu.add_cascade(label="View", menu=db)
    db.add_command(label="Guests", command=lambda: show_data("guest"))
    db.add_command(label="Inventory", command=lambda: show_data("inventory"))
    db.add_command(label="Rooms", command=lambda: show_data("rooms"))
    if role == "admin":
        db.add_command(label="Staff", command=lambda: show_data("staff"))
        db.add_command(label="Users", command=lambda: show_data("user"))

    settings = Menu(mymenu)
    mymenu.add_cascade(label="Settings", menu=settings)
    settings.add_command(label="Sign Out", command=sign_out)
    settings.add_command(label="Exit", command=app.quit)

    # Get user data from session
    user_Name.set(session.get('name', 'Unknown User'))

    # Your main application UI setup
    topbar = Frame(app, width=1500, height=70, bg="lightblue")
    topbar.grid(row=0, column=0, columnspan=3, sticky="ew")
    topbar.grid_columnconfigure(0, weight=1, minsize=500)
    topbar.grid_columnconfigure(1, weight=1, minsize=500)
    topbar.grid_columnconfigure(2, weight=1, minsize=500)
    Label(topbar, text=role.capitalize(), font=("Arial", 24), bg="lightblue", height=2).grid(row=0, column=0, sticky="w", padx=10)
    Label(topbar, text="Welcome to Hotel Management", font=("Arial", 24), bg="lightblue", height=2).grid(row=0, column=1, sticky="n", padx=10)
    Label(topbar, textvariable=user_Name, font=("Arial", 24), bg="lightblue", height=2).grid(row=0, column=2, sticky="e", padx=10)

    # Button Actions
    middlebar = Frame(app, width=1500, height=60)
    middlebar.grid(row=1, column=0, columnspan=3, sticky="ew")
    if role == "user":
        for i in range(3):
            middlebar.grid_columnconfigure(i, weight=1, minsize=500)
        Button(middlebar, text="Guests", font=("Arial", 16), height=2, width=40, command=lambda: button_click("Guest", bottom1)).grid(row=0, column=0)
        Button(middlebar, text="Inventory", font=("Arial", 16), height=2, width=40, command=lambda: button_click("Inventory", bottom1)).grid(row=0, column=1, padx=10)
        Button(middlebar, text="Rooms", font=("Arial", 16), height=2, width=40, command=lambda: button_click("Rooms", bottom1)).grid(row=0, column=2)
    elif role == "admin":
        for i in range(5):
            middlebar.grid_columnconfigure(i, weight=1, minsize=300)
        Button(middlebar, text="Guests", font=("Arial", 16), height=2, width=20, command=lambda: button_click("Guest", bottom1)).grid(row=0, column=0)
        Button(middlebar, text="Inventory", font=("Arial", 16), height=2, width=20, command=lambda: button_click("Inventory", bottom1)).grid(row=0, column=1)
        Button(middlebar, text="Rooms", font=("Arial", 16), height=2, width=20, command=lambda: button_click("Rooms", bottom1)).grid(row=0, column=2)
        Button(middlebar, text="Staff", font=("Arial", 16), height=2, width=20, command=lambda: button_click("Staff", bottom1)).grid(row=0, column=3)
        Button(middlebar, text="Users", font=("Arial", 16), height=2, width=20, command=lambda: button_click("Users", bottom1)).grid(row=0, column=4)

    # Footer
    
    bottom1 = Frame(app, width=1000, height=670)
    bottom1.grid(row=2, column=0, columnspan=2, sticky="ewns")

    app.grid_rowconfigure(2, weight=1, minsize=670)
    bottom2 = Frame(app, width=500)
    bottom2.grid(row=2, column=2, sticky="ewns")

    Button(bottom2, text="Add", font=("Arial", 16), width=40).pack(pady=10)
    Button(bottom2, text="Update", font=("Arial", 16), width=40).pack(pady=10)
    Button(bottom2, text="View", font=("Arial", 16), width=40, command=lambda:View_Action(app)).pack(pady=10)

def View_Action(window):
    global bton_data
    if bton_data == "Guest":
        DisplayData(window, "guest")
    elif bton_data == "Inventory":
        DisplayData(window, "inventory")
    elif bton_data == "Rooms":
        DisplayData(window, "rooms")
    elif bton_data == "Staff":
        DisplayData(window, "staff")
    elif bton_data == "Users":
        DisplayData(window, "users")
    

def sign_out():
    global app, session
    for widget in app.winfo_children():
        widget.destroy()
    session.clear()  # Clear session
    messagebox.showinfo("Signed Out", "You have been signed out successfully.")
    # Return to the login screen
    check_login()

def button_click(collection, window1):
    # Clear the window1 content
    for widget in window1.winfo_children():
        widget.destroy()

    bton_data = collection

    if collection == "Guest":
        label = Label(window1, text="Guests", font=("Arial", 24), width=50)
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Guest Form Fields
        Label(window1, text="Guest ID:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        guest_id_entry = Entry(window1, font=("Arial", 12))
        guest_id_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(window1, text="Name:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        name_entry = Entry(window1, font=("Arial", 12))
        name_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(window1, text="Email:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        email_entry = Entry(window1, font=("Arial", 12))
        email_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(window1, text="Phone:", font=("Arial", 12)).grid(row=4, column=0, sticky="e", padx=10, pady=5)
        phone_entry = Entry(window1, font=("Arial", 12))
        phone_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(window1, text="Address:", font=("Arial", 12)).grid(row=5, column=0, sticky="e", padx=10, pady=5)
        address_entry = Entry(window1, font=("Arial", 12))
        address_entry.grid(row=5, column=1, padx=10, pady=5)

        Label(window1, text="Room No:", font=("Arial", 12)).grid(row=6, column=0, sticky="e", padx=10, pady=5)
        room_no_entry = Entry(window1, font=("Arial", 12))
        room_no_entry.grid(row=6, column=1, padx=10, pady=5)

        Label(window1, text="Check In Date:", font=("Arial", 12)).grid(row=7, column=0, sticky="e", padx=10, pady=5)
        check_in_entry = Entry(window1, font=("Arial", 12))
        check_in_entry.grid(row=7, column=1, padx=10, pady=5)

        Label(window1, text="Check Out Date:", font=("Arial", 12)).grid(row=8, column=0, sticky="e", padx=10, pady=5)
        check_out_entry = Entry(window1, font=("Arial", 12))
        check_out_entry.grid(row=8, column=1, padx=10, pady=5)

        Label(window1, text="Status:", font=("Arial", 12)).grid(row=9, column=0, sticky="e", padx=10, pady=5)
        status_entry = Entry(window1, font=("Arial", 12))
        status_entry.grid(row=9, column=1, padx=10, pady=5)

        # Submit Button to save guest data
        submit_button = Button(window1, text="Submit", font=("Arial", 12))
        submit_button.grid(row=10, column=0, columnspan=2, pady=10)

    elif collection == "Inventory":
        label = Label(window1, text="Inventory", font=("Arial", 24), width=50)
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Inventory Form Fields
        Label(window1, text="Item Name:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        item_entry = Entry(window1, font=("Arial", 12))
        item_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(window1, text="Quantity:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        quantity_entry = Entry(window1, font=("Arial", 12))
        quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(window1, text="Price:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        price_entry = Entry(window1, font=("Arial", 12))
        price_entry.grid(row=3, column=1, padx=10, pady=5)

        # Submit Button to save inventory data
        submit_button = Button(window1, text="Submit", font=("Arial", 12))
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    elif collection == "Rooms":
        label = Label(window1, text="Rooms", font=("Arial", 24), width=50)
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Rooms Form Fields
        Label(window1, text="Room No:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        room_no_entry = Entry(window1, font=("Arial", 12))
        room_no_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(window1, text="Type:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        type_entry = Entry(window1, font=("Arial", 12))
        type_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(window1, text="Status:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        status_entry = Entry(window1, font=("Arial", 12))
        status_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(window1, text="Price:", font=("Arial", 12)).grid(row=4, column=0, sticky="e", padx=10, pady=5)
        price_entry = Entry(window1, font=("Arial", 12))
        price_entry.grid(row=4, column=1, padx=10, pady=5)

        # Submit Button to save room data
        submit_button = Button(window1, text="Submit", font=("Arial", 12))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)
        
    elif collection == "Staff":
        label = Label(window1, text="Staff", font=("Arial", 24), width=50)
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Staff Form Fields
        Label(window1, text="Staff ID:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        staff_id_entry = Entry(window1, font=("Arial", 12))
        staff_id_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(window1, text="Name:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        name_entry = Entry(window1, font=("Arial", 12))
        name_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(window1, text="Role:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        role_entry = Entry(window1, font=("Arial", 12))
        role_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(window1, text="Email:", font=("Arial", 12)).grid(row=4, column=0, sticky="e", padx=10, pady=5)
        email_entry = Entry(window1, font=("Arial", 12))
        email_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(window1, text="Phone:", font=("Arial", 12)).grid(row=5, column=0, sticky="e", padx=10, pady=5)
        phone_entry = Entry(window1, font=("Arial", 12))
        phone_entry.grid(row=5, column=1, padx=10, pady=5)

        Label(window1, text="Address:", font=("Arial", 12)).grid(row=6, column=0, sticky="e", padx=10, pady=5)
        address_entry = Entry(window1, font=("Arial", 12))
        address_entry.grid(row=6, column=1, padx=10, pady=5)

        Label(window1, text="Shift:", font=("Arial", 12)).grid(row=7, column=0, sticky="e", padx=10, pady=5)
        shift_entry = Entry(window1, font=("Arial", 12))
        shift_entry.grid(row=7, column=1, padx=10, pady=5)

        Label(window1, text="Salary:", font=("Arial", 12)).grid(row=8, column=0, sticky="e", padx=10, pady=5)
        salary_entry = Entry(window1, font=("Arial", 12))
        salary_entry.grid(row=8, column=1, padx=10, pady=5)

        Label(window1, text="Status:", font=("Arial", 12)).grid(row=9, column=0, sticky="e", padx=10, pady=5)
        status_entry = Entry(window1, font=("Arial", 12))
        status_entry.grid(row=9, column=1, padx=10, pady=5)

        # Submit Button to save staff data
        submit_button = Button(window1, text="Submit", font=("Arial", 12))
        submit_button.grid(row=10, column=0, columnspan=2, pady=10)
        
    elif collection == "Users":
        label = Label(window1, text="Users", font=("Arial", 24), width=50)
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Users Form Fields
        Label(window1, text="User ID:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        user_id_entry = Entry(window1, font=("Arial", 12))
        user_id_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(window1, text="Username:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        username_entry = Entry(window1, font=("Arial", 12))
        username_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(window1, text="Name:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        name_entry = Entry(window1, font=("Arial", 12))
        name_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(window1, text="Role:", font=("Arial", 12)).grid(row=4, column=0, sticky="e", padx=10, pady=5)
        role_entry = Entry(window1, font=("Arial", 12))
        role_entry.grid(row=4, column=1, padx=10, pady=5)

        # Submit Button to save user data
        submit_button = Button(window1, text="Submit", font=("Arial", 12))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)
        

def check_login():
    if 'user' in session:
        role = session.get('role', 'user')
        show_main(role)
    else:
        Login(app)


# Start by checking login status
check_login()

# Start the Tkinter main loop
app.mainloop()
