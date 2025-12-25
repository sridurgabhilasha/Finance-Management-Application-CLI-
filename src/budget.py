import sqlite3
from .init import DB_PATH

def set_budget(user_id, category_name, amount, month, year):
    """Set or update budget for a category."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get category ID
        cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
        category = cursor.fetchone()
        if not category:
            return False, "Category not found."
        category_id = category[0]
        
        # Insert or update budget
        cursor.execute('''
            INSERT INTO budgets (user_id, category_id, amount, month, year)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, category_id, month, year) 
            DO UPDATE SET amount = excluded.amount
        ''', (user_id, category_id, amount, month, year))
        
        conn.commit()
        conn.close()
        return True, "Budget set successfully."
    except Exception as e:
        return False, str(e)

def get_budgets(user_id, month, year):
    """Get all budgets for a user in a specific month."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.id, c.name, b.amount
        FROM budgets b
        JOIN categories c ON b.category_id = c.id
        WHERE b.user_id = ? AND b.month = ? AND b.year = ?
        ORDER BY c.name
    ''', (user_id, month, year))
    budgets = cursor.fetchall()
    conn.close()
    return budgets

def check_budget_status(user_id, month, year):
    """Check budget status and identify exceeded budgets."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all budgets with actual spending
    cursor.execute('''
        SELECT c.name, b.amount, 
               COALESCE(SUM(t.amount), 0) as spent
        FROM budgets b
        JOIN categories c ON b.category_id = c.id
        LEFT JOIN transactions t ON t.category_id = b.category_id 
            AND t.user_id = b.user_id 
            AND t.type = 'expense'
            AND strftime('%Y', t.date) = ?
            AND strftime('%m', t.date) = ?
        WHERE b.user_id = ? AND b.month = ? AND b.year = ?
        GROUP BY c.name, b.amount
        ORDER BY c.name
    ''', (str(year), f'{month:02d}', user_id, month, year))
    
    budget_status = cursor.fetchall()
    conn.close()
    
    exceeded = []
    within_budget = []
    
    for category, budget_amt, spent in budget_status:
        status = {
            'category': category,
            'budget': budget_amt,
            'spent': spent,
            'remaining': budget_amt - spent,
            'percentage': (spent / budget_amt * 100) if budget_amt > 0 else 0
        }
        
        if spent > budget_amt:
            exceeded.append(status)
        else:
            within_budget.append(status)
    
    return {
        'exceeded': exceeded,
        'within_budget': within_budget
    }

def delete_budget(user_id, budget_id):
    """Delete a budget."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM budgets WHERE id = ? AND user_id = ?', (budget_id, user_id))
        if cursor.rowcount == 0:
            return False, "Budget not found or not owned by user."
        conn.commit()
        conn.close()
        return True, "Budget deleted successfully."
    except Exception as e:
        return False, str(e)
