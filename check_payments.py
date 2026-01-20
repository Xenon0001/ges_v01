import sqlite3

conn = sqlite3.connect('ges_database.db')
cursor = conn.cursor()

# Check table structure
cursor.execute('SELECT sql FROM sqlite_master WHERE type="table" AND name="payments"')
table_sql = cursor.fetchone()
print('Payments table SQL:')
print(table_sql[0] if table_sql else 'Table not found')

# Check data
cursor.execute('SELECT id, status, amount FROM payments')
rows = cursor.fetchall()
print('\nPayments data:')
for row in rows:
    print(f'  ID: {row[0]}, Status: {row[1]}, Amount: {row[2]}')

conn.close()
