import re
import sqlite3
import hashlib
import random

from datetime import datetime
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

conn.execute("PRAGMA foreign_keys = ON")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaction_history (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        transaction_type TEXT NOT NULL CHECK(transaction_type IN ('deposit', 'withdrawal', 'transfer')),
        amount FLOAT NOT NULL,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        balance FLOAT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
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
        bank_menu(user)


  


    
def deposit(id):
    amount = float(input("How muct do yu want to deposit?: "))
    initial_deposit = cursor.execute("""
    SELECT initial_deposit FROM customers WHERE id = ?;
    """, (id,)).fetchone()

    if amount == 0:
        print("Deposit amount must be greater than zero.")
        return
    elif amount < 0:
        print("you cannot deposit amount less than zero(0)")
        return

     
    for cash in initial_deposit:
        cash += amount

    cursor.execute("""
    UPDATE customers 
    SET initial_deposit = ?
    WHERE id = ?;
    """, (cash, id)).fetchone()

    cursor.execute("""
    INSERT INTO transaction_history ( customer_id, transaction_type, amount, balance) 
    VALUES ( ?, ?, ?, ?);
    """, (id, 'deposit', amount, cash))

    conn.commit()

    print(f"Deposit successful! New balance: ${cash}")

def withdrawal(id):
    amount = float(input("How muct do yu want to withdraw?: "))
    initial_deposit = cursor.execute("""
    SELECT initial_deposit FROM customers WHERE id = ?;
    """, (id,)).fetchone()[0]

    if amount == 0:
        print("withrawal amount must be greater than zero.")
        return
    elif amount < 0:
        print("you cannot withdraw amount less than zero(0)")
        return
    elif amount > initial_deposit:
        print("you can not withdraw more than what you have")
        return

     
    for cash in initial_deposit:
        cash -= amount

    cursor.execute("""
    UPDATE customers 
    SET initial_deposit = ?
    WHERE id = ?;
    """, (cash, id)).fetchone()

    cursor.execute("""
    INSERT INTO transaction_history ( customer_id, transaction_type, amount, balance) 
    VALUES ( ?, ?, ?, ?);
    """, (id, 'withdrawal', amount, cash))

    conn.commit()

    print(f"Withdrawal successful! New balance: ${cash}")

def balance(id):
    initial_deposit = cursor.execute("""
    SELECT initial_deposit FROM customers WHERE id = ?;
    """, (id,)).fetchone()[0]
    # initial_deposit = int(initial_deposit)

    print(f"Your current balance is ${initial_deposit}")

def transaction_history(id):
        transactions = cursor.execute("""
        SELECT customer_id, transaction_id, transaction_type, amount, transaction_date, balance
        FROM transaction_history 
        WHERE customer_id = ? 
        ORDER BY transaction_date DESC;
        """, (id,)).fetchall()

        if not transactions:
            print("No transactions found.")
            return

        print("\n********** Transaction History **********\n")
        for cus_id, t_id, t_type, amt, t_date, balance in transactions:
            print(f"customer_id: {cus_id} | Transaction_id: {t_id} | Transaction_type: {t_type.capitalize()} | Amount: ${amt} | Date: {t_date} | Balance: ${balance}")
        print("\n****************************************\n")


def transfer(id):
    receiver_acct = input("Enter the recipient's account number: ").strip()

    receiver = cursor.execute("""SELECT id, initial_deposit 
                                FROM customers 
                                WHERE acct_num = ?;""", (receiver_acct,)).fetchone()
    if not receiver:
        print("Recipient account not found.")
        return
    
    receiver_id, receiver_balance = receiver

    try:
        amount = float(input("Enter the amount to transfer: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    sender_balance = cursor.execute("""SELECT initial_deposit 
                                        FROM customers 
                                        WHERE id = ?;""", (id,)).fetchone()[0]

    if amount <= 0:
        print("Transfer amount must be greater than zero.")
        return
    if amount > sender_balance:
        print("Insufficient funds.")
        return

    new_sender_balance = sender_balance - amount
    cursor.execute("""UPDATE customers 
    SET initial_deposit = ? 
    WHERE id = ?;""", (new_sender_balance, id))

    new_receiver_balance = receiver_balance + amount
    cursor.execute("UPDATE customers SET initial_deposit = ? WHERE id = ?;", (new_receiver_balance, receiver_id))

    cursor.execute("""
        INSERT INTO transaction_history (customer_id, transaction_type, amount, balance) 
        VALUES (?, 'transfer', ?, ?);
    """, (id, amount, new_sender_balance))

    cursor.execute("""
        INSERT INTO transaction_history (customer_id, transaction_type, amount, balance) 
        VALUES (?, 'deposit', ?, ?);
    """, (receiver_id, amount, new_receiver_balance))

    conn.commit()
    print(f"Transfer of ${amount} to account {receiver_acct} successful! Your new balance is ${new_sender_balance}.")



def account_details(id):
    details = cursor.execute("""
        SELECT full_name, username, age, gender, email, acct_num
        FROM customers 
        WHERE id = ? 
        """, (id,)).fetchall()

    print(details)
    return


def bank_menu(user):
    print("\n********************Bank Menu********************\n")

    id, _, _, full_name, _, _, _, _, _, _, acct_num = user
    print(f"Welcome {full_name} your account number is {acct_num}")

    operations = """
1. Deposit
2. Withdrawal
3. Balance Inquiry
4. Transaction History
5. Transfer
6. Account Details
7. Exit
"""
    while True:
        print(operations)

        choice = input("Enter a choice from the menu above: ").strip()
        if choice == "7":
            print("Exiting the operation")
            break
        elif choice not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("invalid option..... please choose from above")
        
        if choice == "1":
            deposit(id)
        elif choice == "2":
            withdrawal(id)
        elif choice == "3":
            balance(id)
        elif choice == "4":
           transaction_history(id)
        elif choice == "5":
            transfer(id)
        elif choice == "6":
            account_details(id)




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

