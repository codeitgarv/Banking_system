import os 
import hashlib
import datetime

# Helper Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_account_number():
    return str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

def write_to_file(filename, data, mode='a'):
    with open(filename, mode) as file:
        file.write(data + "\n")

def read_file_lines(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.readlines()
    return []

def find_account(account_number, password):
    lines = read_file_lines('accounts.txt')
    for line in lines:
        account_data = line.strip().split(',')
        if account_data[0] == account_number and account_data[2] == hash_password(password):
            return account_data
    return None

def update_account_balance(account_number, new_balance):
    accounts = read_file_lines('accounts.txt')
    updated_accounts = []
    for line in accounts:
        account_data = line.strip().split(',')
        if account_data[0] == account_number:
            account_data[3] = str(new_balance)
        updated_accounts.append(','.join(account_data))
    with open('accounts.txt', 'w') as file:
        file.write('\n'.join(updated_accounts) + '\n')

# Core Banking Functions
def create_account():
    name = input("Enter your name: ").strip()
    initial_deposit = float(input("Enter your initial deposit: "))
    password = input("Enter a password: ").strip()

    account_number = generate_account_number()
    hashed_password = hash_password(password)

    account_data = f"{account_number},{name},{hashed_password},{initial_deposit}"
    write_to_file('accounts.txt', account_data)

    print(f"Account created successfully! Your account number is {account_number}. Please save it for future use.")

def login():
    account_number = input("Enter your account number: ").strip()
    password = input("Enter your password: ").strip()

    account_data = find_account(account_number, password)
    if account_data:
        print("Login successful!")
        return account_data
    else:
        print("Invalid account number or password.")
        return None

def deposit(account_data):
    amount = float(input("Enter amount to deposit: "))
    new_balance = float(account_data[3]) + amount
    update_account_balance(account_data[0], new_balance)

    transaction_data = f"{account_data[0]},Deposit,{amount},{datetime.date.today()}"
    write_to_file('transactions.txt', transaction_data)

    print(f"Deposit successful! Current balance: {new_balance}")
    account_data[3] = str(new_balance)  # Update local account balance

def withdraw(account_data):
    amount = float(input("Enter amount to withdraw: "))
    current_balance = float(account_data[3])

    if amount > current_balance:
        print("Insufficient balance.")
    else:
        new_balance = current_balance - amount
        update_account_balance(account_data[0], new_balance)

        transaction_data = f"{account_data[0]},Withdrawal,{amount},{datetime.date.today()}"
        write_to_file('transactions.txt', transaction_data)

        print(f"Withdrawal successful! Current balance: {new_balance}")
        account_data[3] = str(new_balance)  # Update local account balance

def check_balance(account_data):
    print(f"Your current balance is: {account_data[3]}")

def main():
    while True:
        print("\nWelcome to the Banking System!")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            create_account()
        elif choice == '2':
            account_data = login()
            if account_data:
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Logout")

                    user_choice = input("Enter your choice: ").strip()

                    if user_choice == '1':
                        deposit(account_data)
                    elif user_choice == '2':
                        withdraw(account_data)
                    elif user_choice == '3':
                        check_balance(account_data)
                    elif user_choice == '4':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Exiting the system. Have a great day!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
