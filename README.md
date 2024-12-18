# Hotel Management

The Hotel Management System is a comprehensive desktop application designed to streamline and automate various hotel operations. Built with Python, Tkinter for the GUI, and MongoDB for database management, this system ensures efficient handling of tasks such as room bookings, guest records, payments, and more.
---

## Requirements:

### Software:

#### 1. **Python:** 
Python will serve as the programming language for developing the application. It’s powerful, versatile, and widely used for both GUI and database-driven applications.
- **Installation**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Note**: Ensure Python is added to PATH during installation for seamless package management and script execution.

#### 2. **VS Code:**
Visual Studio Code is a lightweight and highly extensible editor, perfect for Python development. 
- **Installation**: [https://code.visualstudio.com/](https://code.visualstudio.com/)
- **Extensions Needed**: Python Extension (for syntax highlighting, debugging, and code completion).

#### 3. **MongoDB:** 
MongoDB is a NoSQL database to store hotel data (e.g., guest records, bookings, rooms, etc.).
- **Installation**: [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
- **Setup Notes**: Follow the installation wizard and ensure MongoDB service is running

### Packages:

#### 1. **pymongo:** 
The pymongo package is a Python driver for MongoDB, enabling interaction with the database.
```
pip install pymongo
``` 

#### 2. **tkinter:** 
When installing Python, check "Add Python to PATH" and ensure "Tcl/Tk and IDLE" is selected during the installation. This enables Tkinter for GUI development.

---

##  Implementation:

### Installation

Step 1: Clone the repository and change directory to that of this project.

```bash
git clone https://github.com/klrab3490/hotel-management.git "Hotel Management"
cd "Hotel Management"
```

Step 2: Setup virtual environment:

- Windows:
```bash
python -m venv env
env\Script\activate.bat
```

- Ubuntu
```bash
python3 -m venv env
source env/bin/activate
```

Step 3: Install `requirements.txt` which contains all the python packages:

```bash
pip install -r requirements.txt
```

### Run

To start the project, use the following command:

```bash
python main.py
```

---
