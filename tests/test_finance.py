import unittest
import sqlite3
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Use a test database
TEST_DB = 'test_finance.db'

from src.auth import register_user, login_user, hash_password
from src.transactions import add_transaction, get_transactions, get_summary
from src.budget import set_budget, get_budgets, check_budget_status
from src.init import initialize_database


class TestFinanceApp(unittest.TestCase):
    """Comprehensive test suite for finance application."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database and test user."""
        # Update DB paths
        import src.init
        import src.auth
        import src.transactions
        import src.budget
        src.init.DB_PATH = TEST_DB
        src.auth.DB_PATH = TEST_DB
        src.transactions.DB_PATH = TEST_DB
        src.budget.DB_PATH = TEST_DB
        
        # Remove existing test database
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        
        # Initialize test database
        initialize_database()
        
        # Register and get test user
        register_user('testuser', 'password123')
        success, cls.user_id = login_user('testuser', 'password123')
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database."""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
    
    # Authentication Tests
    def test_01_register_user(self):
        """Test user registration."""
        success, message = register_user('newuser', 'pass123')
        self.assertTrue(success)
    
    def test_02_register_duplicate(self):
        """Test registering duplicate username."""
        success, message = register_user('testuser', 'password456')
        self.assertFalse(success)
    
    def test_03_login_valid(self):
        """Test login with valid credentials."""
        success, user_id = login_user('testuser', 'password123')
        self.assertTrue(success)
        self.assertIsInstance(user_id, int)
    
    def test_04_login_invalid(self):
        """Test login with invalid password."""
        success, message = login_user('testuser', 'wrongpassword')
        self.assertFalse(success)
    
    def test_05_hash_password(self):
        """Test password hashing."""
        hash1 = hash_password('testpass')
        hash2 = hash_password('testpass')
        self.assertEqual(hash1, hash2)
    
    # Transaction Tests
    def test_10_add_income(self):
        """Test adding income transaction."""
        success, message = add_transaction(self.user_id, 'income', 5000, 'Salary', 'Monthly salary')
        if not success:
            print(f"Add income failed: {message}")
        self.assertTrue(success)
    
    def test_11_add_expense(self):
        """Test adding expense transaction."""
        success, message = add_transaction(self.user_id, 'expense', 500, 'Food', 'Groceries')
        self.assertTrue(success)
    
    def test_12_get_transactions(self):
        """Test retrieving transactions."""
        transactions = get_transactions(self.user_id)
        self.assertGreaterEqual(len(transactions), 2)
    
    def test_13_invalid_category(self):
        """Test adding transaction with invalid category."""
        success, message = add_transaction(self.user_id, 'income', 100, 'InvalidCategory', 'Test')
        self.assertFalse(success)
    
    def test_14_get_summary(self):
        """Test getting financial summary."""
        summary = get_summary(self.user_id)
        self.assertIn('total_income', summary)
        self.assertGreaterEqual(summary['total_income'], 5000)
    
    # Budget Tests
    def test_20_set_budget(self):
        """Test setting a budget."""
        success, message = set_budget(self.user_id, 'Food', 1000, 12, 2025)
        self.assertTrue(success)
    
    def test_21_get_budgets(self):
        """Test retrieving budgets."""
        budgets = get_budgets(self.user_id, 12, 2025)
        self.assertGreaterEqual(len(budgets), 1)
    
    def test_22_check_budget(self):
        """Test checking budget status."""
        status = check_budget_status(self.user_id, 12, 2025)
        self.assertIn('exceeded', status)
        self.assertIn('within_budget', status)


if __name__ == '__main__':
    unittest.main(verbosity=2)
