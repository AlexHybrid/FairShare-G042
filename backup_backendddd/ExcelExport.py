from flask import Flask, render_template, send_file
from openpyxl import Workbook
import os
from database import get_db_connection

export = Flask(__name__)

@export.route('/export')
def export_page():
    return render_template('export.html')


@export.route('/download_excel')
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
    
    file_name = "Temporary_Report.xlsx"
    wb.save(file_name)
    
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    export.run(debug=True, port=5001)