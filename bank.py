import re
import sqlite3
import hashlib
import random

from getpass import getpass


conn = sqlite3.connect("bank_customers.db")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        full_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        initial_deposit FLOAT NOT NULL,
        acct_num INTEGER NOT NULL UNIQUE
    )
    """)


def register():

    print("\n********************Sign Up********************\n")
    while True:

        first_name = input("Enter your first name: ").strip().capitalize()

        if not first_name:
            print("FIrst name field is required")
            continue

        break

    while True:

        last_name = input("Enter your last name: ").strip().capitalize()
        if not last_name:
            print("Last name field is required")
            continue

        break

    while True:

        full_name = f"{first_name} {last_name}"
        
        break
        

    while True:
        username = input("Enter your username: ").strip().casefold()
        if not username:
            print("Username field is required")
            continue
        break

    while True:
        try:
            age = int(input("Enter your age: "))
        except ValueError:
            print("Age must be a number")
            continue
        break

    while True:
        gender = input("Enter your gender: ").strip().capitalize()
        if not gender :
            print("Gender field is required")
            continue
        break

    while True:
        email = input("Enter your email address: ").strip()
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        email_is_valid = re.match(email_pattern, email)
        if not email_is_valid:
            print("Enter a valid email address")
            continue
        break

    while True:
            password = getpass("Enter your password: ").strip()
            if not password:
                print("Password field is required")
                continue

            confirm_password = getpass("Confirm your password: ").strip()
            if not confirm_password:
                print("Confirm Password field is required")
                continue


            if password != confirm_password:
                print("Passwords do not match")
                continue
        
            break

    while True:
        try:
            initial_deposit = float(input("How much do you want to deposit? : "))
            if not initial_deposit:
                print("You have to deposit for your account to be activated")
                continue
            elif initial_deposit < 2000 : 
                print("Your first deposit has to be 2000 and above")
                continue
            break
        except ValueError:
            print("Initial deposit has to be number")
    
    while True:
        
        acct_num = random.randint(10**9, 10**10 - 1)
        break

        

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("""
        INSERT INTO customers (first_name, last_name, full_name, username, age, gender, email, password, initial_deposit, acct_num) VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (first_name, last_name, full_name, username, age, gender, email, hashed_password, initial_deposit, acct_num))
    except sqlite3.IntegrityError as e:
        print("A user with that username already exists.", e)
        return None
    else:
        print("Sign up successful")
        conn.commit()
           
def log_in():

    print("\n********************Log In********************\n")
        
    username = input("Enter your username: ").strip().casefold()
    password = getpass("Enter your password: ").strip()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = cursor.execute("""
    SELECT * FROM customers WHERE username = ? AND password = ?;
    """, (username, hashed_password)).fetchone()

    if user is None:
        print("Invalid username or password.")
        return None
    else:
        print(f"Log in Successful")
        return bank_menu(user)
    
def deposit():
    pass
        
def bank_menu(user):
    print("\n********************Bank Menu********************\n")

    _, _, _, full_name, _, _, _, _, _, _, acct_num= user
    print(f"Welcome {full_name} your account number is {acct_num}")
    operations = """
1. Deposit
2. Withdrawal
3. Balance Inquiry
4. Transaction History
5. Transfer
6. Account Details
"""
    while True:
        print(operations)

        choice = input("Enter a choice from the menu above: ").strip()

        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("invalid option..... please choose from above")


menu = """
1. Register
2. Log In
3. Quit
"""

while True:
    print(menu)
    choice = input("You already have an account? click 2 to log into your account: ")
    if choice == "3":
        print("Exiting Operations")
        break

    if choice not in ["1", "2"]:
        print("Invalid Operation")
        continue

    if choice == "1":
        register()
    elif choice == "2":
        log_in()





# 3. Banking Transactions:
# - Deposit: Allow logged in users to deposit money into their account.
# - Withdrawal: Allow logged in users to withdraw money, ensuring sufficient balance.
# - Balance Inquiry: Display the current balance of the logged in user's account.
# - Transaction History: Provide a history of all transactions performed by the logged in user.
# - Transfer: Allow logged in users to transfer money to other users’ accounts using their account    
#   Number.
# - Account Details: The user should be able to check their account details at once i.e their full name, username, account number.