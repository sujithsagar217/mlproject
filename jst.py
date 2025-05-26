from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["fitness"]

# Check users
print("Users:")
for user in db.users.find():
    print(user)

# Check submissions
print("\nSubmissions:")
for submission in db.submissions.find():
    print(submission)
