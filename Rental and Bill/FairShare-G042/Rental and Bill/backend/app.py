from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS
from database import init_db, get_db_connection
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from our frontend

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize database on startup
init_db()

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

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
            'id':             row['id'],
            'date':           row['date'],
            'room':           row['room'],
            'type':           row['type'],
            'amount':         row['amount'],
            'payment_method': row['payment_method'] or 'Cash',
            'category':       row['category']       or 'Utilities',
            'notes':          row['notes']           or '',
            'receipt_path':   row['receipt_path']    or '',
            'is_recurring':   bool(row['is_recurring']),
            'status':         row['status']          or 'Pending',
        })
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    date           = data.get('date')
    room           = data.get('room')
    type_          = data.get('type')
    amount         = data.get('amount')
    payment_method = data.get('payment_method', 'Cash')
    category       = data.get('category', 'Utilities')
    notes          = data.get('notes', '')
    receipt_path   = data.get('receipt_path', '')
    is_recurring   = 1 if data.get('is_recurring') else 0
    status         = data.get('status', 'Pending')

    if not all([date, room, type_, amount]):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses
            (date, room, type, amount, payment_method, category, notes, receipt_path, is_recurring, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (date, room, type_, float(amount), payment_method, category, notes, receipt_path, is_recurring, status))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'}), 201

@app.route('/api/expenses/upload', methods=['POST'])
def upload_receipt():
    if 'receipt' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['receipt']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_DIR, filename)
        file.save(filepath)
        return jsonify({'receipt_path': filename}), 200
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
