import mysql.connector

try:
    db = mysql.connector.connect(
        port=3306,
        host="localhost",
        user="root",
        password="0974894139Lc",
        database="banking"
    )

    # The actual confirmation check
    if db.is_connected():
        print("✅ Successfully connected to the database!")
        
        # Optional: Print database version to be 100% sure
        db_info = db.get_server_info()
        print(f"Connected to MySQL Server version: {db_info}")

except mysql.connector.Error as err:
    print(f"❌ Connection failed: {err}")