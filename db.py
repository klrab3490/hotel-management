from pymongo import MongoClient
from bson import ObjectId

# MongoDB connection
URL = "mongodb://localhost:27017/"

# MongoDB Client Connection
client = MongoClient(URL)

# Access Database 'HotelMasterDB'
db = client.get_database('Hotel_MasterDB')

# Collections
bookingDB = db.get_collection('booking')
guestDB = db.get_collection('guest')
inventoryDB = db.get_collection('inventory')
roomsDB = db.get_collection('rooms')
staffDB = db.get_collection('staff')
userDB = db.get_collection('user')

# Check if the collection is empty
if inventoryDB.count_documents({}) == 0:
    new_inventory1 = { "item": "Soap", "quantity": 100, "price": 10 }
    new_inventory2 = { "item": "Shampoo", "quantity": 100, "price": 20 }
    new_inventory3 = { "item": "Towel", "quantity": 100, "price": 30 }
    new_inventory4 = { "item": "BedSheet", "quantity": 100, "price": 40 }
    inventoryDB.insert_one(new_inventory1)
    inventoryDB.insert_one(new_inventory2)
    inventoryDB.insert_one(new_inventory3)
    inventoryDB.insert_one(new_inventory4)
    print("Inserted Inventory Data")

if roomsDB.count_documents({}) == 0:
    new_room1 = { "room_no": 101, "type": "Single", "status": "Available", "price": 1000 }
    new_room2 = { "room_no": 102, "type": "Double", "status": "Available", "price": 2000 }
    new_room3 = { "room_no": 103, "type": "Suite", "status": "Available", "price": 3000 }
    new_room4 = { "room_no": 104, "type": "Deluxe", "status": "Available", "price": 4000 }
    new_room5 = { "room_no": 105, "type": "Family", "status": "Available", "price": 5000 }
    roomsDB.insert_one(new_room1)
    roomsDB.insert_one(new_room2)
    roomsDB.insert_one(new_room3)
    roomsDB.insert_one(new_room4)
    roomsDB.insert_one(new_room5)
    print("Inserted Rooms Data")

if staffDB.count_documents({}) == 0:
    new_staff1 = { "staff_id": "S001", "name": "John Doe", "role": "Receptionist", "email": "john.doe@example.com", "phone": "9123456789", "address": "123 Main Street, City", "shift": "Morning", "salary": 22000, "status": "active" }
    new_staff2 = { "staff_id": "S002", "name": "Jane Smith", "role": "Cleaner", "email": "jane.smith@example.com", "phone": "9234567890", "address": "456 Elm Street, Suburb", "shift": "Evening", "salary": 14000, "status": "active" }
    new_staff3 = { "staff_id": "S003", "name": "Alice Johnson", "role": "Manager", "email": "alice.johnson@example.com", "phone": "9345678901", "address": "789 Oak Avenue, Town", "shift": "Morning", "salary": 55000, "status": "on leave" }
    new_staff4 = { "staff_id": "S004", "name": "Bob Brown", "role": "Chef", "email": "bob.brown@example.com", "phone": "9456789012", "address": "135 Pine Road, Village", "shift": "Morning", "salary": 32000, "status": "resigned" }
    new_staff5 = { "staff_id": "S005", "name": "Charlie Davis", "role": "Security", "email": "charlie.davis@example.com", "phone": "9567890123", "address": "246 Maple Lane, Metro", "shift": "Night", "salary": 18000, "status": "active" }
    new_staff6 = { "staff_id": "S006", "name": "Eva Martinez", "role": "Receptionist", "email": "eva.martinez@example.com", "phone": "9678901234", "address": "357 Cedar Court, City Center", "shift": "Evening", "salary": 23000, "status": "active" }
    new_staff7 = { "staff_id": "S007", "name": "Frank Wilson", "role": "Cleaner", "email": "frank.wilson@example.com", "phone": "9789012345", "address": "123 Main Street, City", "shift": "Night", "salary": 14000, "status": "on leave" }
    new_staff8 = { "staff_id": "S008", "name": "Grace Lee", "role": "Manager", "email": "grace.lee@example.com", "phone": "9890123456", "address": "456 Elm Street, Suburb", "shift": "Morning", "salary": 60000, "status": "active" }
    new_staff9 = { "staff_id": "S009", "name": "Henry Harris", "role": "Chef", "email": "henry.harris@example.com", "phone": "9901234567", "address": "789 Oak Avenue, Town", "shift": "Evening", "salary": 29000, "status": "active" }
    new_staff10 = { "staff_id": "S010", "name": "Isla Turner", "role": "Security", "email": "isla.turner@example.com", "phone": "9012345678", "address": "135 Pine Road, Village", "shift": "Night", "salary": 19000, "status": "active" }
    staffDB.insert_one(new_staff1)
    staffDB.insert_one(new_staff2)
    staffDB.insert_one(new_staff3)
    staffDB.insert_one(new_staff4)
    staffDB.insert_one(new_staff5)
    staffDB.insert_one(new_staff6)
    staffDB.insert_one(new_staff7)
    staffDB.insert_one(new_staff8)
    staffDB.insert_one(new_staff9)
    staffDB.insert_one(new_staff10)
    print("Inserted Staff Data")

if userDB.count_documents({}) == 0:  
    new_user1 = { "username": "admin", "password": "admin", "name": "Rahul A B(admin)", "role": "admin" }
    new_user2 = { "username": "user", "password": "user", "name": "Rahul A B(user)", "role": "user" }
    userDB.insert_one(new_user1)
    userDB.insert_one(new_user2)
    print("Inserted User Data")

# Session dictionary to store logged-in user details
session = {}

def login(username, password):
    user = userDB.find_one({ "username": username })
    if user:
        if user.get("password") == password:
            session['user'] = username
            session['userID'] = str(user["_id"])
            session['name'] = user["name"]
            session['role'] = user["role"]
            return True, "Login"
        else:
            return False, "Invalid Password"
    else:
        return False, "User Not Found"

def getDB(collection):
    if 'user' in session:
        # Define a dictionary for the collections
        collection_map = {
            "guest": guestDB,
            "inventory": inventoryDB,
            "rooms": roomsDB,
            "staff": staffDB,
            "user": userDB
        }
        
        # Check if the collection exists in the map
        if collection in collection_map:
            data = collection_map[collection].find()
            return True, data, "Data Fetched"
        else:
            return False, False, "No Data Fetched"
    else:
        return False, False, "User Not Logged In"
    
def addDB(collection, data):
    if 'user' in session:  # Check if a user is logged in
        # Define a dictionary for the collections
        collection_map = {
            "guest": guestDB,
            "inventory": inventoryDB,
            "rooms": roomsDB,
            "staff": staffDB,
            "user": userDB
        }
        print(data)

        # Validate collection
        if collection in collection_map:
            try:
                # Perform the database insertion
                result = collection_map[collection].insert_one(data)
                return True, str(result.inserted_id), "Data successfully added"
            except Exception as e:
                return False, None, f"An unexpected error occurred: {str(e)}"
        else:
            return False, None, "Invalid collection name specified"
    else:
        return False, None, "User not logged in"

def updateDB(collection, query, update):
    if 'user' in session:  # Check if a user is logged in
        # Define a dictionary for the collections
        collection_map = {
            "guest": guestDB,
            "inventory": inventoryDB,
            "rooms": roomsDB,
            "staff": staffDB,
            "user": userDB
        }
        query = { "_id": ObjectId(query) } # Convert the query string to ObjectId

        # Fix the field
        print("Data Arrived In Update: ", update)
        update_data = map_update_data(collection, update)
        print("Data to be updated in Mongo:",update_data)

        # Validate collection
        if collection in collection_map:
            try:
                # Perform the database update
                result = collection_map[collection].update_one(query, {"$set": update_data})
                if result.modified_count > 0:
                    return True, "Data successfully updated"
                else:
                    return False, "No matching data found or no changes made"
            except Exception as e:
                return False, f"An unexpected error occurred: {str(e)}"
        else:
            return False, "Invalid collection name specified"
    else:
        return False, "User not logged in"
    
def map_update_data(collection_name, update):
    # Define keys
    collection_keys = {
        "guest": ("ID", "Name", "Email", "Phone", "Address", "Room No", "Check In", "Check Out", "Status"),
        "inventory": ("ID", "Item Name", "Quantity", "Price"),
        "rooms": ("ID", "Room No", "Type", "Status", "Price"),
        "staff": ("ID", "Name", "Role", "Email", "Phone", "Address", "Shift", "Salary", "Status"),
        "user": ("ID", "Name", "Username", "Role")
    }
    
    database_keys = {
        "guest": ["_id", "name", "email", "phone", "address", "room_no", "checkin_date", "checkout_date", "status"],
        "inventory": ["_id", "item", "quantity", "price"],
        "rooms": ["_id", "room_no", "type", "status", "price"],
        "staff": ["_id", "staff_id", "name", "role", "email", "phone", "address", "shift", "salary", "status"],
        "user": ["_id", "username", "password", "name", "role"]
    }
    
    # Fields to convert to integers
    int_fields = {"price", "quantity", "salary"}

    # Create a mapping between the keys
    key_mapping = dict(zip(collection_keys[collection_name], database_keys[collection_name]))
    
    # Map the update data to the new keys and handle type conversion
    update_data = {}
    for key, value in update.items():
        if key in key_mapping:
            db_key = key_mapping[key]
            if db_key in int_fields:
                # Convert to int if it's in the int_fields
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError(f"Value for '{db_key}' must be an integer, got '{value}'")
            update_data[db_key] = value
    
    return update_data


