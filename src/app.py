from .init import initialize_database
from .auth import register_user, login_user
from .transactions import add_transaction, get_transactions, update_transaction, delete_transaction, get_summary, get_categories
import getpass

def main_menu():
    """Display main menu."""
    print("\nPersonal Finance Management Application")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Choose an option: ").strip()
    return choice

def user_menu():
    """Display user menu."""
    print("\nUser Menu")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. List Transactions")
    print("4. Update Transaction")
    print("5. Delete Transaction")
    print("6. Generate Report")
    print("7. Logout")
    choice = input("Choose an option: ").strip()
    return choice

def register():
    """Handle user registration."""
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password: ")
    success, message = register_user(username, password)
    print(message)

def login():
    """Handle user login."""
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password: ")
    success, user_id = login_user(username, password)
    if success:
        print("Login successful.")
        return user_id
    else:
        print(user_id)  # error message
        return None

def add_income(user_id):
    """Add income."""
    categories = get_categories()
    print("Available categories:", ', '.join(categories))
    amount = float(input("Enter amount: "))
    category = input("Enter category: ").strip()
    description = input("Enter description (optional): ").strip()
    success, message = add_transaction(user_id, 'income', amount, category, description)
    print(message)

def add_expense(user_id):
    """Add expense."""
    categories = get_categories()
    print("Available categories:", ', '.join(categories))
    amount = float(input("Enter amount: "))
    category = input("Enter category: ").strip()
    description = input("Enter description (optional): ").strip()
    success, message = add_transaction(user_id, 'expense', amount, category, description)
    print(message)

def list_transactions(user_id):
    """List transactions."""
    transactions = get_transactions(user_id)
    if not transactions:
        print("No transactions found.")
    else:
        print("ID | Type | Amount | Category | Description | Date")
        for t in transactions:
            print(f"{t[0]} | {t[1]} | {t[2]} | {t[3]} | {t[4]} | {t[5]}")

def update_transaction_menu(user_id):
    """Update transaction."""
    list_transactions(user_id)
    try:
        transaction_id = int(input("Enter transaction ID to update: "))
        print("Enter new values (leave blank to keep current):")
        amount_str = input("New amount: ").strip()
        category = input("New category: ").strip()
        description = input("New description: ").strip()
        
        kwargs = {}
        if amount_str:
            kwargs['amount'] = float(amount_str)
        if category:
            kwargs['category'] = category
        if description:
            kwargs['description'] = description
        
        if not kwargs:
            print("No changes made.")
            return
        
        success, message = update_transaction(transaction_id, user_id, **kwargs)
        print(message)
    except ValueError:
        print("Invalid input.")

def delete_transaction_menu(user_id):
    """Delete transaction."""
    list_transactions(user_id)
    try:
        transaction_id = int(input("Enter transaction ID to delete: "))
        success, message = delete_transaction(transaction_id, user_id)
        print(message)
    except ValueError:
        print("Invalid input.")

def generate_report(user_id):
    """Generate financial report."""
    summary = get_summary(user_id)
    print("Financial Report:")
    print(f"Total Income: ${summary['total_income']:.2f}")
    print(f"Total Expenses: ${summary['total_expenses']:.2f}")
    print(f"Balance: ${summary['balance']:.2f}")

def run():
    """Main application entry point."""
    # Initialize database
    initialize_database()
    
    current_user = None
    
    while True:
        if current_user is None:
            choice = main_menu()
            if choice == '1':
                register()
            elif choice == '2':
                current_user = login()
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")
        else:
            choice = user_menu()
            if choice == '1':
                add_income(current_user)
            elif choice == '2':
                add_expense(current_user)
            elif choice == '3':
                list_transactions(current_user)
            elif choice == '4':
                update_transaction_menu(current_user)
            elif choice == '5':
                delete_transaction_menu(current_user)
            elif choice == '6':
                generate_report(current_user)
            elif choice == '7':
                print("Logging out...")
                current_user = None
            else:
                print("Invalid choice.")
