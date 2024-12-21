from tkinter import *
from tkinter import messagebox, ttk
from db import session, login, getDB, addDB, updateDB

class HotelManagementApp:
    def __init__(self):
        self.app = Tk()
        self.app.title("Hotel Management")
        self.app.geometry("1500x800+0+0")

        self.session = session

        self.user_Name = StringVar()
        self.DB_submit = StringVar()

        self.bton_data = ""
        self.addBtn = None
        self.updateBtn = None
        self.viewBtn = None
        self.closeBtn = None
        self.data = {}

        self.init_variables()
        self.check_login()
        self.app.mainloop()

    def init_variables(self):
        self.guest_id = StringVar()
        self.name = StringVar()
        self.email = StringVar()
        self.phone = StringVar()
        self.address = StringVar()
        self.room_no = StringVar()
        self.check_in = StringVar()
        self.check_out = StringVar()
        self.status = StringVar()
        self.item = StringVar()
        self.quantity = StringVar()
        self.price = StringVar()
        self.type = StringVar()
        self.shift = StringVar()
        self.salary = StringVar()
        self.role = StringVar()
        self.password = StringVar()
        self.username = StringVar()
        self.staff_id = StringVar()

    def check_login(self):
        if 'user' in self.session:
            role = self.session.get('role', 'user')
            self.show_main(role)
        else:
            Login(self)

    def show_main(self, role):
        if 'user' not in self.session:
            messagebox.showerror("Error", "No user logged in.")
            self.app.quit()
            return

        for widget in self.app.winfo_children():
            widget.destroy()

        self.build_menu(role)
        self.build_topbar(role)
        self.build_middlebar(role)
        self.build_footer()

    def build_menu(self, role):
        mymenu = Menu(self.app)
        self.app.config(menu=mymenu)

        db_menu = Menu(mymenu)
        mymenu.add_cascade(label="View", menu=db_menu)
        db_menu.add_command(label="Guests", command=lambda: self.show_data("guest"))
        db_menu.add_command(label="Inventory", command=lambda: self.show_data("inventory"))
        db_menu.add_command(label="Rooms", command=lambda: self.show_data("rooms"))
        if role == "admin":
            db_menu.add_command(label="Staff", command=lambda: self.show_data("staff"))
            db_menu.add_command(label="Users", command=lambda: self.show_data("user"))

        settings_menu = Menu(mymenu)
        mymenu.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Sign Out", command=self.sign_out)
        settings_menu.add_command(label="Exit", command=self.app.quit)

    def build_topbar(self, role):
        topbar = Frame(self.app, width=1500, height=70, bg="lightblue")
        topbar.grid(row=0, column=0, columnspan=3, sticky="ew")
        topbar.grid_columnconfigure(0, weight=1, minsize=500)
        topbar.grid_columnconfigure(1, weight=1, minsize=500)
        topbar.grid_columnconfigure(2, weight=1, minsize=500)

        Label(topbar, text=role.capitalize(), font=("Arial", 24), bg="lightblue", height=2).grid(row=0, column=0, sticky="w", padx=10)
        Label(topbar, text="Welcome to Hotel Management", font=("Arial", 24), bg="lightblue", height=2).grid(row=0, column=1, sticky="n", padx=10)
        Label(topbar, textvariable=self.user_Name, font=("Arial", 24), bg="lightblue", height=2).grid(row=0, column=2, sticky="e", padx=10)

        self.user_Name.set(self.session.get('name', 'Unknown User'))

    def build_middlebar(self, role):
        middlebar = Frame(self.app, width=1500, height=60)
        middlebar.grid(row=1, column=0, columnspan=3, sticky="ew")

        button_config = {
            "Guests": ("Guest", 0),
            "Inventory": ("Inventory", 1),
            "Rooms": ("Rooms", 2),
        }

        if role == "admin":
            button_config.update({
                "Staff": ("Staff", 3),
                "Users": ("Users", 4),
            })

        for text, (collection, column) in button_config.items():
            Button(middlebar, text=text, font=("Arial", 16), height=2, width=20, command=lambda c=collection: self.button_click(c)).grid(row=0, column=column)

    def build_footer(self):
        self.bottom1 = Frame(self.app, width=1000, height=670)
        self.bottom1.grid(row=2, column=0, columnspan=2, sticky="ewns")
        self.app.grid_rowconfigure(2, weight=1, minsize=670)
        
        self.bottom2 = Frame(self.app, width=500)
        self.bottom2.grid(row=2, column=2, sticky="ewns")

        self.addBtn = Button(self.bottom2, text="Add", font=("Arial", 16), width=40, command=self.add_action)
        self.addBtn.pack(pady=10)
        self.addBtn.config(state=DISABLED)

        self.updateBtn = Button(self.bottom2, text="Update", font=("Arial", 16), width=40, command=self.update_action)
        self.updateBtn.pack(pady=10)
        self.updateBtn.config(state=DISABLED)

        self.viewBtn = Button(self.bottom2, text="View", font=("Arial", 16), width=40, command=self.view_action)
        self.viewBtn.pack(pady=10)
        self.viewBtn.config(state=DISABLED)

        self.closeBtn = Button(self.bottom2, text="Close", font=("Arial", 16), width=40, command=self.clear_action)
        self.closeBtn.pack(pady=10)
        self.closeBtn.config(state=DISABLED)

    def button_click(self, collection):
        self.bton_data = collection
        self.show_form(collection)
        self.update_button_state(ACTIVE)

    def show_form(self, collection):
        for widget in self.bottom1.winfo_children():
            widget.destroy()

        form_fields = {
            "Guest": ["Name", "Email", "Phone", "Address", "Room No", "Status"],
            "Inventory": ["Item", "Quantity", "Price"],
            "Rooms": ["Room No", "Type", "Status", "Price"],
            "Staff": ["Staff ID", "Name", "Role", "Email", "Phone", "Shift", "Salary", "Status"],
            "Users": ["Username", "Password", "Name", "Role"]
        }

        fields = form_fields.get(collection, [])

        for idx, field in enumerate(fields):
            label = Label(self.bottom1, text=f"{field}:", font=("Arial", 12))
            label.grid(row=idx, column=0, sticky="e", padx=10, pady=5)

            entry_var = getattr(self, field.lower().replace(" ", "_"), None)
            if entry_var is not None:
                entry = Entry(self.bottom1, textvariable=entry_var, font=("Arial", 12))
                entry.grid(row=idx, column=1, padx=10, pady=5)

        self.dataBtn = Button(self.bottom1, text="Add", font=("Arial", 16), command=self.submit_data)
        self.dataBtn.grid(row=len(fields), column=0, columnspan=2, pady=10)

        label1 = Label(self.bottom1, text="Data: ", font=("Arial", 12))
        label2 = Label(self.bottom1, textvariable=self.DB_submit, font=("Arial", 12))
        label1.grid(row=len(fields) + 1, column=0, pady=10)
        label2.grid(row=len(fields) + 1, column=1, pady=10)

    def update_button_state(self, state):
        for btn in [self.addBtn, self.updateBtn, self.viewBtn, self.closeBtn]:
            btn.config(state=state)

    def show_data(self, collection):
        success, data, message = getDB(collection)
        if success:
            DisplayData(self.app, data, collection)
        else:
            messagebox.showerror("Error", message)
    
    def show_update_data(self, collection):
        success, data, message = getDB(collection)
        if success:
            DisplayData(self.app, data, collection, update=True)
        else:
            messagebox.showerror("Error", message)

    def sign_out(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.session.clear()
        messagebox.showinfo("Signed Out", "You have been signed out successfully.")
        self.check_login()

    def add_action(self):
        if not self.bton_data:
            messagebox.showerror("Error", "No data type selected for update.")
            return

        if self.data:
            success, message = addDB(self.bton_data.lower(), self.data)
            if success:
                messagebox.showinfo("Update Successful", message)
            else:
                messagebox.showerror("Update Failed", message)

    def update_action(self):
        self.show_update_data(self.bton_data.lower())

    def view_action(self):
        self.show_data(self.bton_data.lower())

    def clear_action(self):
        self.bton_data = ""
        self.data = {}
        self.DB_submit.set("")
        self.destroy_form()
        self.update_button_state(DISABLED)

    def destroy_form(self):
        for widget in self.bottom1.winfo_children():
            widget.destroy()

    def submit_data(self):
        print("Submit data", self.bton_data)
        self.collection = self.bton_data.lower()
        if self.collection == "guest":
            data = {
                "name": self.name.get(),
                "email": self.email.get(),
                "phone": self.phone.get(),
                "address": self.address.get(),
                "room_no": self.room_no.get(),
                "check_in": self.check_in.get(),
                "check_out": self.check_out.get(),
                "status": self.status.get()
            }
        elif self.collection == "inventory":
            data = {
                "item": self.item.get(),
                "quantity": self.quantity.get(),
                "price": self.price.get()
            }
        elif self.collection == "rooms":
            data = {
                "room_no": self.room_no.get(),
                "type": self.type.get(),
                "status": self.status.get(),
                "price": self.price.get()
            }
        elif self.collection == "staff":
            data = {
                "staff_id": self.staff_id.get(),
                "name": self.name.get(),
                "role": self.role.get(),
                "email": self.email.get(),
                "phone": self.phone.get(),
                "address": self.address.get(),
                "shift": self.shift.get(),
                "salary": self.salary.get(),
                "status": self.status.get()
            }
        elif self.collection == "user":
            data = {
                "username": self.username.get(),
                "password": self.password.get(),
                "name": self.name.get(),
                "role": self.role.get()
            }
        else:
            messagebox.showerror("Error", "Data collection not implemented for this type.")
        
        self.data = data
        self.DB_submit.set(data)

class Login:
    def __init__(self, app):
        self.app = app
        self.master = app.app
        self.window = Toplevel(self.master)
        self.window.title("Login")
        self.window.geometry("300x200")

        self.window.transient(self.master)
        self.window.grab_set()

        Label(self.window, text="Login", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        Label(self.window, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.username = Entry(self.window, font=("Arial", 12))
        self.username.grid(row=1, column=1, padx=10, pady=5)

        Label(self.window, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.password = Entry(self.window, font=("Arial", 12), show="*")
        self.password.grid(row=2, column=1, padx=10, pady=5)

        Button(self.window, text="Login", font=("Arial", 12), command=self.handle_login).grid(row=3, column=0, columnspan=2)
        Button(self.window, text="Exit", font=("Arial", 12), command=self.master.destroy).grid(row=4, column=0, columnspan=2)

    def handle_login(self):
        username = self.username.get()
        password = self.password.get()
        success, message = login(username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.window.destroy()
            self.app.check_login()
        else:
            messagebox.showerror("Error", message)

class DisplayData:
    def __init__(self, parent, data, collection, update=False):
        self.window = Toplevel(parent)
        self.window.title(f"{collection.capitalize()} Data")
        self.window.geometry("900x400")

        self.tree = ttk.Treeview(self.window)

        self.parent = parent
        self.data = data
        self.collection = collection

        # Field mapping for collections
        collection_map = {
            "guest": ("ID", "Name", "Email", "Phone", "Address", "Room No", "Check In", "Check Out", "Status"),
            "inventory": ("ID", "Item Name", "Quantity", "Price"),
            "rooms": ("ID", "Room No", "Type", "Status", "Price"),
            "staff": ("ID", "Name", "Role", "Email", "Phone", "Address", "Shift", "Salary", "Status"),
            "user": ("ID", "Name", "Username", "Role")
        }

        if collection in collection_map:
            columns = collection_map[collection]
            self.tree["columns"] = columns
            self.tree["show"] = "headings"

            for col in columns:
                self.tree.heading(col, text=col, anchor="w")
                self.tree.column(col, anchor="w", width=100)

            for item in data:
                self.tree.insert("", "end", values=tuple(item.values()))

        self.tree.pack(expand=True, fill="both")
        close_button = ttk.Button(self.window, text="Close", command=self.window.destroy)
        close_button.pack(pady=10)

        if update==True:
            self.tree.bind("<Double-1>", self.open_update_window)
            

    def open_update_window(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            row_data = self.tree.item(selected_item[0], "values")
            field_names = [col for col in self.tree["columns"]]

            # Map the row data to field names
            selected_data = {field: value for field, value in zip(field_names, row_data)}

            # Open the UpdateDisplayData window
            UpdateDisplayData(self.parent, self.collection, selected_data)

            # Close the current DisplayData window
            self.window.destroy()

class UpdateDisplayData:
    def __init__(self, parent, collection, selected_data):
        self.parent = parent
        self.collection = collection
        self.selected_data = selected_data
        self.window = Toplevel(parent)
        self.window.title(f"Update {collection.capitalize()} Data")
        self.window.geometry("400x400")

        # Field mapping for collections
        collection_kes = {
            "guest": ("ID", "Name", "Email", "Phone", "Address", "Room No", "Check In", "Check Out", "Status"),
            "inventory": ("ID", "Item Name", "Quantity", "Price"),
            "rooms": ("ID", "Room No", "Type", "Status", "Price"),
            "staff": ("ID", "Name", "Role", "Email", "Phone", "Address", "Shift", "Salary", "Status"),
            "user": ("ID", "Name", "Username", "Role")
        }

        self.fields = collection_kes.get(collection, [])
        self.form_vars = {}

        # Update form layout
        for idx, field in enumerate(self.fields):
            label = Label(self.window, text=f"{field}:", font=("Arial", 12))
            label.grid(row=idx, column=0, sticky="e", padx=10, pady=5)

            entry_var = StringVar()
            entry = Entry(self.window, textvariable=entry_var, font=("Arial", 12))
            entry.grid(row=idx, column=1, padx=10, pady=5)

            # Pre-fill with selected data
            entry_var.set(selected_data.get(field, ""))  # Use the field name to access the value
            self.form_vars[field] = entry_var

        # Buttons
        self.update_btn = Button(self.window, text="Update", font=("Arial", 16), command=self.update_data)
        self.update_btn.grid(row=len(self.fields), column=0, columnspan=2, pady=10)

        self.close_btn = Button(self.window, text="Close", font=("Arial", 16), command=self.window.destroy)
        self.close_btn.grid(row=len(self.fields) + 1, column=0, columnspan=2, pady=10)

    def update_data(self):
        # Collect updated data from the form
        updated_data = {field: var.get() for field, var in self.form_vars.items()}

        # Explicitly check for '_id' as the database ID field
        id_field = "ID"
        record_id = updated_data.pop(id_field, None)

        if not record_id:
            messagebox.showerror("Error", "Record ID (_id) is missing. Cannot update.")
            return

        # Call the updateDB function with the corrected ID field
        success, message = updateDB(self.collection, record_id, updated_data)
        if success:
            messagebox.showinfo("Success", "Data updated successfully.")
            self.window.destroy()
        else:
            messagebox.showerror("Error", message)

if __name__ == "__main__":
    HotelManagementApp()
