# Personal Finance Management Application (CLI)

A comprehensive command-line application for managing personal finances, tracking income and expenses, setting budgets, and generating detailed financial reports.

## Features

### 1. User Authentication
- Secure user registration with unique usernames
- Password hashing using SHA-256
- Login functionality for user sessions

### 2. Transaction Management
- Add income and expense transactions
- Categorize transactions (Food, Rent, Salary, Entertainment, etc.)
- Update existing transactions
- Delete transactions
- List all transactions with filtering options

### 3. Financial Reports
- Generate summary reports (total income, expenses, balance)
- Monthly financial reports with category breakdown
- Yearly financial reports with monthly trends
- Category-wise spending analysis

### 4. Budgeting System
- Set monthly budgets for different categories
- View all budgets for a specific month
- Check budget status with visual indicators
- Get notifications when budgets are exceeded
- Track spending percentage against budgets

### 5. Data Management
- SQLite database for persistent storage
- Backup database to timestamped files
- Restore database from backups
- Export transactions to CSV format
- Automatic backup creation before restore operations

## Installation

### Prerequisites
- Python 3.7 or higher
- SQLite3 (usually comes with Python)

### Setup Instructions

1. **Clone or download the repository:**
   ```bash
   cd /path/to/Finance-Management-Application-CLI-
   ```

2. **No additional dependencies required** - the application uses only Python standard libraries.

3. **Run the application:**
   ```bash
   python3 main.py
   ```

## Usage Guide

### Starting the Application

Run the application using:
```bash
python3 main.py
```

You'll see the main menu:
```
Personal Finance Management Application
1. Register
2. Login
3. Exit
```

### First-Time Setup

1. **Register a new account:**
   - Choose option 1 (Register)
   - Enter a unique username
   - Enter a secure password (input is hidden)

2. **Login:**
   - Choose option 2 (Login)
   - Enter your username and password

### User Menu Options

After logging in, you'll have access to these features:

#### 1. Add Income
- Enter the amount
- Select a category (e.g., Salary, Freelance, Investment)
- Add an optional description
- Transaction is automatically dated

#### 2. Add Expense
- Enter the amount
- Select a category (e.g., Food, Rent, Entertainment)
- Add an optional description
- Transaction is automatically dated

#### 3. List Transactions
- View all your transactions
- Shows ID, Type, Amount, Category, Description, and Date
- Sorted by date (newest first)

#### 4. Update Transaction
- View list of transactions
- Enter transaction ID to update
- Modify amount, category, or description
- Leave fields blank to keep current values

#### 5. Delete Transaction
- View list of transactions
- Enter transaction ID to delete
- Transaction is permanently removed

#### 6. Generate Summary Report
- View total income, expenses, and current balance
- Quick overview of your financial status

#### 7. Generate Monthly Report
- Enter year and month (e.g., 2025, 12)
- View income and expenses for that month
- See category breakdown for income and expenses
- Calculate monthly savings

#### 8. Generate Yearly Report
- Enter year (e.g., 2025)
- View total income and expenses for the year
- See monthly breakdown showing trends
- View category-wise spending analysis
- Calculate annual savings

#### 9. Set Budget
- Select a category
- Enter budget amount
- Specify month and year
- Update existing budgets automatically

#### 10. View Budgets
- Enter month and year
- See all budgets set for that period
- View budget amounts for each category

#### 11. Check Budget Status
- Enter month and year
- See budgets that have been exceeded (⚠️)
- See budgets within limits (✓)
- View spending percentage for each category
- See remaining budget amounts

#### 12. Backup Database
- Creates a timestamped backup file
- Stored in 'backups' directory
- Includes all user data and transactions

#### 13. Restore Database
- View list of available backups
- Select backup to restore
- Current database is backed up before restore
- Requires confirmation

#### 14. Export Transactions to CSV
- Export all your transactions to a CSV file
- Default filename: transactions_export.csv
- Can be opened in Excel or other spreadsheet applications

#### 15. Logout
- Safely logout and return to main menu

## Default Categories

The application comes with these pre-configured categories:
- Food
- Rent
- Salary
- Entertainment
- Transportation
- Utilities
- Healthcare
- Other

## Database Structure

The application uses SQLite with the following tables:

### users
- `id`: Primary key
- `username`: Unique username
- `password_hash`: SHA-256 hashed password

### categories
- `id`: Primary key
- `name`: Category name (unique)

### transactions
- `id`: Primary key
- `user_id`: Foreign key to users
- `type`: 'income' or 'expense'
- `amount`: Transaction amount
- `category_id`: Foreign key to categories
- `description`: Optional description
- `date`: Transaction date

### budgets
- `id`: Primary key
- `user_id`: Foreign key to users
- `category_id`: Foreign key to categories
- `amount`: Budget amount
- `month`: Month (1-12)
- `year`: Year
- Unique constraint on (user_id, category_id, month, year)

## File Structure

```
Finance-Management-Application-CLI-/
├── main.py                 # Application entry point
├── cmd_args.py             # Command-line argument parser (legacy)
├── README.md               # This file
├── LICENSE                 # License information
├── src/
│   ├── __init__.py        # Package initialization
│   ├── init.py            # Database initialization
│   ├── auth.py            # Authentication functions
│   ├── app.py             # Main application logic
│   ├── transactions.py    # Transaction management
│   ├── budget.py          # Budget management
│   └── backup.py          # Backup and restore functions
├── tests/
│   ├── __init__.py        # Test package initialization
│   └── test_finance.py    # Unit tests
├── static/                 # Static files (if any)
├── backups/               # Database backups (created automatically)
└── finance.db             # SQLite database (created on first run)
```

## Running Tests

To run the unit tests:

```bash
python3 -m pytest tests/test_finance.py -v
```

Or using unittest:

```bash
python3 tests/test_finance.py
```

The test suite covers:
- User registration and authentication
- Transaction operations (add, update, delete)
- Budget management
- Database backup and restore
- Input validation

## Security Notes

- Passwords are hashed using SHA-256 before storage
- Password input is hidden during entry (using getpass)
- Each user can only access their own data
- Database backups are created before restore operations

## Tips and Best Practices

1. **Regular Backups**: Use the backup feature regularly to protect your data
2. **Budget Planning**: Set realistic monthly budgets and check status regularly
3. **Categorization**: Use consistent categories for better reporting
4. **Monthly Reviews**: Generate monthly reports to track spending patterns
5. **Descriptions**: Add descriptions to transactions for better tracking

## Troubleshooting

### Database Issues
- If the database becomes corrupted, restore from a backup
- Delete `finance.db` to start fresh (all data will be lost)

### Permission Errors
- Ensure you have write permissions in the application directory
- Check that the backups directory can be created

### Import Errors
- Make sure you're running Python 3.7 or higher
- Verify you're in the correct directory when running the application

## Future Enhancements

Potential features for future versions:
- Multiple currency support
- Recurring transactions
- Bill reminders
- Graphical charts and visualizations
- Mobile app integration
- Cloud synchronization
- Advanced reporting (custom date ranges)
- Category management (add/edit/delete)

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for new features
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Contact the development team

## Version History

### Version 1.0.0 (Current)
- User authentication system
- Income and expense tracking
- Monthly and yearly reports
- Budget management with notifications
- Database backup and restore
- CSV export functionality
- Comprehensive test suite

---

**Happy budgeting! Take control of your finances today!** 💰📊