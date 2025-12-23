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