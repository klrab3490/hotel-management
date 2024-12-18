# Hotel Management System

The **Hotel Management System** is a comprehensive desktop application designed to streamline and automate various hotel operations. Built with Python, Tkinter for the GUI, and MongoDB for database management, this system ensures efficient handling of tasks such as room bookings, guest records, payments, and more.

---

## Features

- **Guest Registration**: Add new guests with personal details.
- **Room Booking**: Book rooms for guests with availability checking.
- **Payment Management**: Track payments and balances.
- **Room Management**: Add, update, and remove rooms.
- **Database Integration**: Uses MongoDB to store guest data, booking details, and room information.
- **User-friendly GUI**: Built with Tkinter for a simple, intuitive interface.

---

## Requirements

### Software:

1. **Python**  
   Python will serve as the programming language for developing the application. It’s powerful, versatile, and widely used for both GUI and database-driven applications.  
   - **Installation**: [Download Python](https://www.python.org/downloads/)  
   - **Note**: Ensure Python is added to PATH during installation for seamless package management and script execution.

2. **VS Code**  
   Visual Studio Code is a lightweight and highly extensible editor, perfect for Python development.  
   - **Installation**: [Download VS Code](https://code.visualstudio.com/)  
   - **Extensions Needed**: Python Extension (for syntax highlighting, debugging, and code completion).

3. **MongoDB**  
   MongoDB is a NoSQL database to store hotel data (e.g., guest records, bookings, rooms, etc.).  
   - **Installation**: [Download MongoDB](https://www.mongodb.com/try/download/community)  
   - **Setup Notes**: Follow the installation wizard and ensure MongoDB service is running.

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/klrab3490/hotel-management.git "Hotel Management"
cd "Hotel Management"
```

### Step 2: Setup Virtual Environment

- **Windows**:
  ```bash
  python -m venv env
  env\Scripts\activate.bat
  ```
- **Ubuntu**:
  ```bash
  python3 -m venv env
  source env/bin/activate
  ```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

To start the project, use the following command:

```bash
python main.py
```

---

## Related Topics

1. **Tkinter Documentation**:  
   Learn more about Tkinter and its widgets:  
   [https://docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html)

2. **MongoDB Setup and Usage**:  
   How to set up and interact with MongoDB:  
   [https://pymongo.readthedocs.io/](https://pymongo.readthedocs.io/)

3. **Python Virtual Environments**:  
   Learn how to work with Python virtual environments:  
   [https://docs.python.org/3/tutorial/venv.html](https://docs.python.org/3/tutorial/venv.html)

4. **VS Code Python Extension**:  
   Enhance your Python coding experience in VS Code:  
   [https://marketplace.visualstudio.com/items?itemName=ms-python.python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- **Tkinter**: For building the GUI interface.
- **MongoDB**: For providing a robust and flexible database solution.
- **Python**: For the foundation of the project and its vast library support.

---

Feel free to contribute or reach out if you have any questions or suggestions!
