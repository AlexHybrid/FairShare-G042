from flask import Flask, request, jsonify, send_from_directory, send_file
import os
from flask_cors import CORS
from database import init_db, get_db_connection
from werkzeug.utils import secure_filename
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

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

@app.route('/download_excel')
def download_excel():
    wb = Workbook()
    sheet = wb.active
    sheet.title = "Data Bil"
    
    sheet.append(["Date", "Room", "Type", "Amount", "Payment Method", "Category", "Status", "Notes"])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        sheet.append([
            row['date'],
            row['room'],
            row['type'],
            row['amount'],
            row['payment_method'] or 'Cash',
            row['category'] or 'Utilities',
            row['status'] or 'Pending',
            row['notes'] or ''
        ])
    
    file_name = "The report of Fairshare.xlsx"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    wb.save(file_path)
    
    return send_file(file_path, as_attachment=True, download_name="The report of Fairshare.xlsx")

@app.route('/download_pdf')
def download_pdf():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT date, room, type, amount, status FROM expenses')
    rows = cursor.fetchall()
    conn.close()
    
    current_data = [["Date", "Room", "Type", "Amount", "Status"]]
    for row in rows:
        current_data.append([
            row['date'],
            row['room'],
            row['type'],
            f"RM{row['amount']:.2f}",
            row['status'] or 'Pending'
        ])
        
    file_name = "FairShare_Live_Report.pdf"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    pdf_canvas = SimpleDocTemplate(file_path)
    pdf_table = Table(current_data)
    table_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    pdf_table.setStyle(table_style)
    pdf_canvas.build([pdf_table])
    
    return send_file(file_path, as_attachment=True, download_name="FairShare_Live_Report.pdf")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
