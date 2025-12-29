import sqlite3
import shutil
import os
from datetime import datetime
from .init import DB_PATH

def backup_database(backup_dir='backups'):
    """Backup the database to a file."""
    try:
        # Create backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'finance_backup_{timestamp}.db')
        
        # Copy database file
        shutil.copy2(DB_PATH, backup_file)
        
        return True, f"Database backed up successfully to {backup_file}"
    except Exception as e:
        return False, f"Backup failed: {str(e)}"

def restore_database(backup_file):
    """Restore database from a backup file."""
    try:
        if not os.path.exists(backup_file):
            return False, "Backup file not found."
        
        # Create a backup of current database before restoring
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        current_backup = f'{DB_PATH}.before_restore_{timestamp}.bak'
        shutil.copy2(DB_PATH, current_backup)
        
        # Restore from backup
        shutil.copy2(backup_file, DB_PATH)
        
        return True, f"Database restored successfully from {backup_file}"
    except Exception as e:
        return False, f"Restore failed: {str(e)}"

def list_backups(backup_dir='backups'):
    """List all available backup files."""
    try:
        if not os.path.exists(backup_dir):
            return []
        
        backup_files = []
        for filename in os.listdir(backup_dir):
            if filename.startswith('finance_backup_') and filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                file_stat = os.stat(filepath)
                size_mb = file_stat.st_size / (1024 * 1024)
                mod_time = datetime.fromtimestamp(file_stat.st_mtime)
                backup_files.append({
                    'filename': filename,
                    'filepath': filepath,
                    'size': size_mb,
                    'modified': mod_time
                })
        
        # Sort by modification time, newest first
        backup_files.sort(key=lambda x: x['modified'], reverse=True)
        return backup_files
    except Exception as e:
        return []

def export_data_csv(user_id, output_file='transactions_export.csv'):
    """Export user transactions to CSV file."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, t.date, t.type, c.name, t.amount, t.description
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = ?
            ORDER BY t.date DESC
        ''', (user_id,))
        
        transactions = cursor.fetchall()
        conn.close()
        
        # Write to CSV
        with open(output_file, 'w') as f:
            f.write("ID,Date,Type,Category,Amount,Description\n")
            for t in transactions:
                # Escape description if it contains commas
                desc = f'"{t[5]}"' if ',' in str(t[5]) else t[5]
                f.write(f"{t[0]},{t[1]},{t[2]},{t[3]},{t[4]},{desc}\n")
        
        return True, f"Transactions exported to {output_file}"
    except Exception as e:
        return False, f"Export failed: {str(e)}"
