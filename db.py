from pymongo import MongoClient

# MongoDB connection
URL = "mongodb://localhost:27017/"

# MongoDB Client Connection
client = MongoClient(URL)

# Access Database 'HotelMasterDB'
db = client['HotelMasterDB']

# Collections
guestDB = db['guest']
inventoryDB = db['inventory']
roomsDB = db['rooms']
staffDB = db['staff']
userDB = db['user']

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
