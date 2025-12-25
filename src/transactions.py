import sqlite3
from .init import DB_PATH

def add_transaction(user_id, type_, amount, category_name, description):
    """Add a new transaction."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get category ID
        cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
        category = cursor.fetchone()
        if not category:
            return False, "Category not found."
        category_id = category[0]
        
        # Insert transaction
        cursor.execute('''
            INSERT INTO transactions (user_id, type, amount, category_id, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, type_, amount, category_id, description))
        
        conn.commit()
        conn.close()
        return True, "Transaction added successfully."
    except Exception as e:
        return False, str(e)

def get_transactions(user_id):
    """Get all transactions for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.id, t.type, t.amount, c.name, t.description, t.date
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ?
        ORDER BY t.date DESC
    ''', (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def update_transaction(transaction_id, user_id, **kwargs):
    """Update a transaction."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if transaction belongs to user
        cursor.execute('SELECT id FROM transactions WHERE id = ? AND user_id = ?', (transaction_id, user_id))
        if not cursor.fetchone():
            return False, "Transaction not found or not owned by user."
        
        # Build update query
        update_fields = []
        values = []
        if 'amount' in kwargs:
            update_fields.append('amount = ?')
            values.append(kwargs['amount'])
        if 'category_name' in kwargs:
            cursor.execute('SELECT id FROM categories WHERE name = ?', (kwargs['category_name'],))
            category = cursor.fetchone()
            if not category:
                return False, "Category not found."
            update_fields.append('category_id = ?')
            values.append(category[0])
        if 'description' in kwargs:
            update_fields.append('description = ?')
            values.append(kwargs['description'])
        
        if not update_fields:
            return False, "No fields to update."
        
        query = f'UPDATE transactions SET {", ".join(update_fields)} WHERE id = ? AND user_id = ?'
        values.extend([transaction_id, user_id])
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return True, "Transaction updated successfully."
    except Exception as e:
        return False, str(e)

def delete_transaction(transaction_id, user_id):
    """Delete a transaction."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE id = ? AND user_id = ?', (transaction_id, user_id))
        if cursor.rowcount == 0:
            return False, "Transaction not found or not owned by user."
        conn.commit()
        conn.close()
        return True, "Transaction deleted successfully."
    except Exception as e:
        return False, str(e)

def get_categories():
    """Get all categories."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM categories')
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def get_summary(user_id):
    """Get financial summary for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total income
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = ?', (user_id, 'income'))
    total_income = cursor.fetchone()[0] or 0
    
    # Total expenses
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = ?', (user_id, 'expense'))
    total_expenses = cursor.fetchone()[0] or 0
    
    balance = total_income - total_expenses
    
    conn.close()
    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance
    }

def get_monthly_report(user_id, year, month):
    """Get monthly financial report."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get transactions for the specified month
    cursor.execute('''
        SELECT t.type, c.name, SUM(t.amount) as total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ? 
        AND strftime('%Y', t.date) = ? 
        AND strftime('%m', t.date) = ?
        GROUP BY t.type, c.name
        ORDER BY t.type, total DESC
    ''', (user_id, str(year), f'{month:02d}'))
    
    category_breakdown = cursor.fetchall()
    
    # Get total income
    cursor.execute('''
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND type = 'income'
        AND strftime('%Y', date) = ? 
        AND strftime('%m', date) = ?
    ''', (user_id, str(year), f'{month:02d}'))
    total_income = cursor.fetchone()[0] or 0
    
    # Get total expenses
    cursor.execute('''
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND type = 'expense'
        AND strftime('%Y', date) = ? 
        AND strftime('%m', date) = ?
    ''', (user_id, str(year), f'{month:02d}'))
    total_expenses = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'category_breakdown': category_breakdown,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': total_income - total_expenses
    }

def get_yearly_report(user_id, year):
    """Get yearly financial report."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get transactions by month
    cursor.execute('''
        SELECT strftime('%m', t.date) as month, t.type, SUM(t.amount) as total
        FROM transactions t
        WHERE t.user_id = ? AND strftime('%Y', t.date) = ?
        GROUP BY month, t.type
        ORDER BY month
    ''', (user_id, str(year)))
    
    monthly_data = cursor.fetchall()
    
    # Get category breakdown
    cursor.execute('''
        SELECT t.type, c.name, SUM(t.amount) as total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ? AND strftime('%Y', t.date) = ?
        GROUP BY t.type, c.name
        ORDER BY t.type, total DESC
    ''', (user_id, str(year)))
    
    category_breakdown = cursor.fetchall()
    
    # Get total income
    cursor.execute('''
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND type = 'income'
        AND strftime('%Y', date) = ?
    ''', (user_id, str(year)))
    total_income = cursor.fetchone()[0] or 0
    
    # Get total expenses
    cursor.execute('''
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND type = 'expense'
        AND strftime('%Y', date) = ?
    ''', (user_id, str(year)))
    total_expenses = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'monthly_data': monthly_data,
        'category_breakdown': category_breakdown,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': total_income - total_expenses
    }