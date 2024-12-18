from pymongo import MongoClient

# MongoDB connection
URL = "mongodb://localhost:27017/"

# MongoDB Client Connection
client = MongoClient(URL)

# Access Database 'HotelMasterDB'
db = client['HotelMasterDB']
userDB = db['user']

# Session dictionary to store logged-in user details
session = {}

def login(username, password):
    user = userDB.find_one({ "username": username })
    if user:
        if user.get("password") == password:
            session['user'] = username
            session['userID'] = str(user["_id"])
            return True, "Login"
        else:
            return False, "Invalid Password"
    else:
        return False, "User Not Found"