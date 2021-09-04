from config import db


# test for database access

# db.users.insert_one({"name": "Sarah", "email": "srvilladoz@gmail.com"})
# db.users.insert_one({"name": "Genie", "email": "geniethemaltipoo@gmail.com"})
# db.users.insert_one({"name": "Pebbles", "email": "pebblestheschnauzer@gmail.com"})

cursor = db.users.find({"name": "Pebbles"})
for user in cursor:
    print(user)