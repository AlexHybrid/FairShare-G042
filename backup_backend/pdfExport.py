from flask import Flask, render_template, send_file
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os

export = Flask(__name__)

from database import get_db_connection

#---Dynamic Data Bridge---
def get_user_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT date, room, type, amount, status FROM expenses')
    rows = cursor.fetchall()
    conn.close()
    
    data = [["Date", "Room", "Type", "Amount", "Status"]]
    for row in rows:
        data.append([
            row['date'],
            row['room'],
            row['type'],
            f"RM{row['amount']:.2f}",
            row['status'] or 'Pending'
        ])
    return data

@export.route('/export')
def export_page():
    # Renders the HTML page with the export buttons
    return render_template('export.html')

@export.route('/download_pdf')
def download_pdf():
    current_data = get_user_data()
    file_name = "FairShare_Live_Report.pdf"
    pdf_canvas = SimpleDocTemplate(file_name)
    pdf_table = Table(current_data)
    table_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    pdf_table.setStyle(table_style)
    pdf_canvas.build([pdf_table])
    
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    # Running on port 5002 to avoid conflict if it run both simultaneously
    export.run(debug=True, port=5002)