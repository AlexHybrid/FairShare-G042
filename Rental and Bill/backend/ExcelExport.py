from flask import Flask, render_template, send_file
from openpyxl import Workbook
import os

export = Flask(__name__)

@export.route('/export')
def export_page():
    return render_template('export.html')


@export.route('/download_excel')
def download_excel():
    wb = Workbook()
    sheet = wb.active
    sheet.title = "Data Bil"
    
    sheet.append(["Date", "Room", "Name", "Amount"])
    sheet.append(["07 Jan 2026", "Room A", "Ali Bin Ghazali", 300])
    
    file_name = "Temporary_Report.xlsx"
    wb.save(file_name)
    
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    export.run(debug=True)