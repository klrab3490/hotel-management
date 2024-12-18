from pymongo import MongoClient

# MongoDB connection
URL = "mongodb://localhost:27017/"

# MongoDB Client Connection
client = MongoClient(URL)

# Access Database 'HotelMasterDB'
db = client.get_database('HotelMasterDB')

# Collections
guestDB = db.get_collection('guest')
inventoryDB = db.get_collection('inventory')
roomsDB = db.get_collection('rooms')
staffDB = db.get_collection('staff')
userDB = db.get_collection('user')

if userDB.count_documents({}) == 0:  # Check if the collection is empty
    new_user1 = { "username": "admin", "password": "admin", "name": "Rahul A B(admin)", "role": "admin" }
    new_user2 = { "username": "user", "password": "user", "name": "Rahul A B(user)", "role": "user" }
    userDB.insert_one(new_user1)
    userDB.insert_one(new_user2)
    print("Inserted Data")

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
