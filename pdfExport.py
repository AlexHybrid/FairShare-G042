from flask import Flask, render_template, send_file
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os

export = Flask(__name__)

#---Dynamic Data Bridge---
def get_user_data():
    # Simulating 'live' data pulled from the FairShare database
    live_data = [
        ["Date", "Room", "Name", "Amount"],
        ["15 May 2026", "Room A", "Muhammad Alif", "$150"],
        ["15 May 2026", "Room A", "Housemate 1", "$50"],
        ["16 May 2026", "Room C", "Housemate 2", "$100"]
    ]
    return live_data

