import pickle
import os

ACCOUNTS_FILE = 'accounts.pkl'
USERS_FILE = 'users.pkl'

# ---------- HELPER FUNCTIONS ----------
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return {}

def save_data(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

# ---------- INITIALIZATION ----------
def init_data():
    if not os.path.exists(ACCOUNTS_FILE):
        save_data({}, ACCOUNTS_FILE)
    if not os.path.exists(USERS_FILE):
        save_data({}, USERS_FILE)

# ---------- ACCOUNT CREATION ----------
def create_account():
    accounts = load_data(ACCOUNTS_FILE)
    users = load_data(USERS_FILE)

    accNo = int(input("Enter desired account number: "))
    if accNo in accounts:
        print(" Account number already exists.")
        return None

    name = input("Enter your name: ")
    while True:
        acc_type = input("Enter account type [C/S]: ").upper()
        if acc_type in ['C', 'S']:
            break
        print("Invalid type! Choose 'C' for Current or 'S' for Saving.")

    while True:
        deposit = int(input("Enter initial deposit: "))
        if (acc_type == 'S' and deposit >= 500) or (acc_type == 'C' and deposit >= 1000):
            break
        print("Minimum ₹500 for Saving and ₹1000 for Current.")

    password = input("Set a password for your account: ")

    accounts[accNo] = {'name': name, 'type': acc_type, 'deposit': deposit}
    users[accNo] = password

    save_data(accounts, ACCOUNTS_FILE)
    save_data(users, USERS_FILE)
    print("\n Account created successfully!")
    return accNo

# ---------- LOGIN ----------
def verify_user(accNo, password):
    users = load_data(USERS_FILE)
    if accNo not in users:
        return "no_account"
    if users[accNo] == password:
        return "ok"
    return "wrong_pass"

# ---------- ACCOUNT OPERATIONS ----------
def show_balance(accNo):
    accounts = load_data(ACCOUNTS_FILE)
    if accNo in accounts:
        print(f"Available balance: ₹{accounts[accNo]['deposit']}")
    else:
        print("Account not found.")

def deposit_or_withdraw(accNo, action):
    accounts = load_data(ACCOUNTS_FILE)
    if accNo not in accounts:
        print("Account not found.")
        return

    amount = int(input(f"Enter amount to {action}: "))
    balance = accounts[accNo]['deposit']

    if action == "deposit":
        balance += amount
    elif action == "withdraw":
        if amount > balance:
            print("!! Insufficient funds.")
            return
        balance -= amount

    accounts[accNo]['deposit'] = balance
    save_data(accounts, ACCOUNTS_FILE)
    print(f"{action.capitalize()} successful. New balance: ₹{balance}")

def modify_account(accNo):
    accounts = load_data(ACCOUNTS_FILE)
    if accNo in accounts:
        name = input("Enter new name: ")
        while True:
            acc_type = input("Enter new type [C/S]: ").upper()
            if acc_type in ['C', 'S']:
                break
            print("Invalid type! Use C or S.")
        deposit = int(input("Enter new balance: "))

        accounts[accNo] = {'name': name, 'type': acc_type, 'deposit': deposit}
        save_data(accounts, ACCOUNTS_FILE)
        print("Account updated.")
    else:
        print("Account not found.")

def delete_account(accNo):
    accounts = load_data(ACCOUNTS_FILE)
    users = load_data(USERS_FILE)

    if accNo in accounts:
        del accounts[accNo]
        del users[accNo]
        save_data(accounts, ACCOUNTS_FILE)
        save_data(users, USERS_FILE)
        print("Account deleted.")
    else:
        print("Account not found.")

def display_all_accounts():
    accounts = load_data(ACCOUNTS_FILE)
    if accounts:
        print(f"{'AccNo':<10}{'Name':<20}{'Type':<10}{'Balance':<10}")
        for accNo, info in accounts.items():
            print(f"{accNo:<10}{info['name']:<20}{info['type']:<10}{info['deposit']:<10}")
    else:
        print("No accounts found.")

# ---------- MENUS ----------
def user_menu(accNo):
    while True:
        print("\n-- USER MENU --")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Balance Enquiry")
        print("4. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            deposit_or_withdraw(accNo, 'deposit')
        elif choice == '2':
            deposit_or_withdraw(accNo, 'withdraw')
        elif choice == '3':
            show_balance(accNo)
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

def admin_menu():
    while True:
        print("\n-- ADMIN MENU --")
        print("1. View All Account Holders")
        print("2. Modify Account")
        print("3. Close Account")
        print("4. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            display_all_accounts()
        elif choice == '2':
            accNo = int(input("Enter account number to modify: "))
            modify_account(accNo)
        elif choice == '3':
            accNo = int(input("Enter account number to delete: "))
            delete_account(accNo)
            break
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

# ---------- MAIN PROGRAM ----------
def main():
    init_data()
    while True:
        print("\n========= LOGIN MENU =========")
        print("1. Admin")
        print("2. Existing User")
        print("3. New User")
        print("4. Exit")
        print("===============================")
        choice = input("Choose an option: ")

        if choice == '1':
            password = input("Enter admin password: ")
            if password == 'admin123':
                admin_menu()
            else:
                print("Wrong password.")
        elif choice == '2':
            accNo = int(input("Enter your account number: "))
            password = input("Enter your password: ")
            res = verify_user(accNo, password)
            if res == "ok":
                user_menu(accNo)
            elif res == "wrong_pass":
                print("Incorrect Password")
            elif res == "no_account":
                print("No such account found")
        elif choice == '3':
            accNo = create_account()
            if accNo:
                user_menu(accNo)
        elif choice == '4':
            print("Thank you for using the Bank Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
