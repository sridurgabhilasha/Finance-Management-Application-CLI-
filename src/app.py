from .init import initialize_database
from .auth import register_user, login_user
from .transactions import add_transaction, get_transactions, update_transaction, delete_transaction, get_summary, get_categories, get_monthly_report, get_yearly_report
from .budget import set_budget, get_budgets, check_budget_status, delete_budget
from .backup import backup_database, restore_database, list_backups, export_data_csv
import getpass
from datetime import datetime

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
    print("6. Generate Summary Report")
    print("7. Generate Monthly Report")
    print("8. Generate Yearly Report")
    print("9. Set Budget")
    print("10. View Budgets")
    print("11. Check Budget Status")
    print("12. Backup Database")
    print("13. Restore Database")
    print("14. Export Transactions to CSV")
    print("15. Logout")
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
    """Generate financial summary report."""
    summary = get_summary(user_id)
    print("\nFinancial Summary Report:")
    print(f"Total Income: ${summary['total_income']:.2f}")
    print(f"Total Expenses: ${summary['total_expenses']:.2f}")
    print(f"Balance: ${summary['balance']:.2f}")

def generate_monthly_report(user_id):
    """Generate monthly financial report."""
    try:
        year = int(input("Enter year (e.g., 2025): "))
        month = int(input("Enter month (1-12): "))
        
        if month < 1 or month > 12:
            print("Invalid month. Please enter a value between 1 and 12.")
            return
        
        report = get_monthly_report(user_id, year, month)
        
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        print(f"\nMonthly Report for {month_names[month]} {year}")
        print("=" * 50)
        print(f"Total Income: ${report['total_income']:.2f}")
        print(f"Total Expenses: ${report['total_expenses']:.2f}")
        print(f"Savings: ${report['savings']:.2f}")
        
        if report['category_breakdown']:
            print("\nCategory Breakdown:")
            current_type = None
            for type_, category, total in report['category_breakdown']:
                if type_ != current_type:
                    print(f"\n{type_.upper()}:")
                    current_type = type_
                print(f"  {category}: ${total:.2f}")
        else:
            print("\nNo transactions found for this period.")
    except ValueError:
        print("Invalid input. Please enter numeric values.")

def generate_yearly_report(user_id):
    """Generate yearly financial report."""
    try:
        year = int(input("Enter year (e.g., 2025): "))
        
        report = get_yearly_report(user_id, year)
        
        print(f"\nYearly Report for {year}")
        print("=" * 50)
        print(f"Total Income: ${report['total_income']:.2f}")
        print(f"Total Expenses: ${report['total_expenses']:.2f}")
        print(f"Savings: ${report['savings']:.2f}")
        
        if report['monthly_data']:
            print("\nMonthly Breakdown:")
            month_names = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            monthly_summary = {}
            for month, type_, total in report['monthly_data']:
                month_num = int(month)
                if month_num not in monthly_summary:
                    monthly_summary[month_num] = {'income': 0, 'expense': 0}
                monthly_summary[month_num][type_] = total
            
            for month_num in sorted(monthly_summary.keys()):
                data = monthly_summary[month_num]
                savings = data['income'] - data['expense']
                print(f"  {month_names[month_num]}: Income: ${data['income']:.2f}, "
                      f"Expenses: ${data['expense']:.2f}, Savings: ${savings:.2f}")
        
        if report['category_breakdown']:
            print("\nCategory Breakdown:")
            current_type = None
            for type_, category, total in report['category_breakdown']:
                if type_ != current_type:
                    print(f"\n{type_.upper()}:")
                    current_type = type_
                print(f"  {category}: ${total:.2f}")
        
        if not report['monthly_data'] and not report['category_breakdown']:
            print("\nNo transactions found for this year.")
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

def set_budget_menu(user_id):
    """Set budget for a category."""
    try:
        categories = get_categories()
        print("Available categories:", ', '.join(categories))
        category = input("Enter category name: ").strip()
        amount = float(input("Enter budget amount: "))
        month = int(input("Enter month (1-12): "))
        year = int(input("Enter year (e.g., 2025): "))
        
        if month < 1 or month > 12:
            print("Invalid month. Please enter a value between 1 and 12.")
            return
        
        success, message = set_budget(user_id, category, amount, month, year)
        print(message)
    except ValueError:
        print("Invalid input. Please enter valid numeric values.")

def view_budgets_menu(user_id):
    """View budgets for a specific month."""
    try:
        month = int(input("Enter month (1-12): "))
        year = int(input("Enter year (e.g., 2025): "))
        
        if month < 1 or month > 12:
            print("Invalid month. Please enter a value between 1 and 12.")
            return
        
        budgets = get_budgets(user_id, month, year)
        
        if not budgets:
            print(f"No budgets set for {month}/{year}.")
        else:
            month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
            print(f"\nBudgets for {month_names[month]} {year}:")
            print("ID | Category | Budget Amount")
            for budget in budgets:
                print(f"{budget[0]} | {budget[1]} | ${budget[2]:.2f}")
    except ValueError:
        print("Invalid input. Please enter numeric values.")

def check_budget_menu(user_id):
    """Check budget status and show exceeded budgets."""
    try:
        month = int(input("Enter month (1-12): "))
        year = int(input("Enter year (e.g., 2025): "))
        
        if month < 1 or month > 12:
            print("Invalid month. Please enter a value between 1 and 12.")
            return
        
        status = check_budget_status(user_id, month, year)
        
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        print(f"\nBudget Status for {month_names[month]} {year}:")
        print("=" * 60)
        
        if status['exceeded']:
            print("\n⚠️  BUDGETS EXCEEDED:")
            for item in status['exceeded']:
                print(f"  {item['category']}:")
                print(f"    Budget: ${item['budget']:.2f}")
                print(f"    Spent: ${item['spent']:.2f}")
                print(f"    Over by: ${abs(item['remaining']):.2f} ({item['percentage']:.1f}%)")
        
        if status['within_budget']:
            print("\n✓ BUDGETS WITHIN LIMIT:")
            for item in status['within_budget']:
                print(f"  {item['category']}:")
                print(f"    Budget: ${item['budget']:.2f}")
                print(f"    Spent: ${item['spent']:.2f}")
                print(f"    Remaining: ${item['remaining']:.2f} ({item['percentage']:.1f}%)")
        
        if not status['exceeded'] and not status['within_budget']:
            print("No budgets set for this period.")
    except ValueError:
        print("Invalid input. Please enter numeric values.")

def backup_menu(user_id):
    """Backup database."""
    success, message = backup_database()
    print(message)

def restore_menu(user_id):
    """Restore database from backup."""
    backups = list_backups()
    
    if not backups:
        print("No backup files found.")
        return
    
    print("\nAvailable Backups:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup['filename']}")
        print(f"   Size: {backup['size']:.2f} MB")
        print(f"   Modified: {backup['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        choice = int(input("\nEnter backup number to restore (0 to cancel): "))
        if choice == 0:
            print("Restore cancelled.")
            return
        
        if 1 <= choice <= len(backups):
            backup_file = backups[choice - 1]['filepath']
            confirm = input(f"Are you sure you want to restore from {backups[choice - 1]['filename']}? (yes/no): ")
            if confirm.lower() == 'yes':
                success, message = restore_database(backup_file)
                print(message)
                if success:
                    print("Please restart the application for changes to take effect.")
            else:
                print("Restore cancelled.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

def export_csv_menu(user_id):
    """Export transactions to CSV."""
    filename = input("Enter output filename (default: transactions_export.csv): ").strip()
    if not filename:
        filename = 'transactions_export.csv'
    
    success, message = export_data_csv(user_id, filename)
    print(message)

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
                generate_monthly_report(current_user)
            elif choice == '8':
                generate_yearly_report(current_user)
            elif choice == '9':
                set_budget_menu(current_user)
            elif choice == '10':
                view_budgets_menu(current_user)
            elif choice == '11':
                check_budget_menu(current_user)
            elif choice == '12':
                backup_menu(current_user)
            elif choice == '13':
                restore_menu(current_user)
            elif choice == '14':
                export_csv_menu(current_user)
            elif choice == '15':
                print("Logging out...")
                current_user = None
            else:
                print("Invalid choice.")
