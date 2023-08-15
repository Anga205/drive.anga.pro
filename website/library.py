import re, sqlite3, random, time, sqlite3

def is_valid_email(email):
    # Regular expression pattern for validating email addresses
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Use the re.match function to check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False

def setup_rx_db():
    # 1) Attempt to connect to "rx.db" or create a new database if it doesn't exist
    try:
        connection = sqlite3.connect('rx.db')
    except sqlite3.Error as e:
        raise Exception(f"Error connecting to 'rx.db': {e}")
    
    cursor = connection.cursor()
    
    # 2) Check if 'accounts' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts';")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        # 3) Create 'accounts' table with the specified columns
        try:
            cursor.execute('''CREATE TABLE accounts (
                                username TEXT,
                                email TEXT PRIMARY KEY,
                                password TEXT,
                                data TEXT
                            )''')
            print("'accounts' table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating 'accounts' table: {e}")
        finally:
            connection.commit()
    else:
        print("'accounts' table already exists.")

    # Close the connection
    connection.close()

def new_user_signup(username: str, email: str, password: str) -> bool:
    # 1) Attempt to connect to "rx.db" or create a new database if it doesn't exist
    try:
        connection = sqlite3.connect('rx.db')
    except sqlite3.Error as e:
        return f"Error connecting to 'rx.db': {e}"
    
    cursor = connection.cursor()
    
    # Check if email already exists in the 'accounts' table
    cursor.execute("SELECT email FROM accounts WHERE email = ?;", (email,))
    existing_email = cursor.fetchone()
    if existing_email:
        return "Email id already exists"
    
    # Check username length
    if len(username) < 3 or len(username) > 16: 
        return "Username must be between 3 and 16 characters long"
    
    try:
        # Insert new user details into the 'accounts' table
        cursor.execute("INSERT INTO accounts (username, email, password) VALUES (?, ?, ?);",
                       (username, email, password))
        connection.commit()
        print("User signup successful.")
        return True
    except sqlite3.Error as e:
        return f"Error inserting user data: {e}"
    finally:
        # Close the connection
        connection.close()

def login_user(email: str, password: str) -> list:

    # Attempt to connect to "rx.db" or create a new database if it doesn't exist
    try:
        connection = sqlite3.connect('rx.db')
        print("Connected to 'rx.db'")
    except sqlite3.Error as e:
        print(f"Error connecting to 'rx.db': {e}")
        return [False, "Error connecting to the database"]
    
    cursor = connection.cursor()
    
    # Check if the email exists in the 'accounts' table
    cursor.execute("SELECT username, password FROM accounts WHERE email = ?;", (email,))
    user_info = cursor.fetchone()
    
    if not user_info:
        connection.close()
        return [False, "Email does not exist"]
    
    username, stored_password = user_info
    
    if stored_password == password:
        connection.close()
        return [True, username]
    else:
        connection.close()
        return [False, "Email and password do not match"]
