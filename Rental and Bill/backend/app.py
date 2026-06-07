from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, get_db_connection

app = Flask(__name__)
CORS(app) # Allow cross-origin requests from our frontend

# Initialize database on startup
init_db()

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    rows = cursor.fetchall()
    conn.close()
    
    expenses = []
    for row in rows:
        expenses.append({
            'id': row['id'],
            'date': row['date'],
            'room': row['room'],
            'type': row['type'],
            'amount': row['amount']
        })
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    date = data.get('date')
    room = data.get('room')
    type_ = data.get('type')
    amount = data.get('amount')
    
    if not all([date, room, type_, amount]):
        return jsonify({'error': 'Missing data'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, room, type, amount)
        VALUES (?, ?, ?, ?)
    ''', (date, room, type_, float(amount)))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
