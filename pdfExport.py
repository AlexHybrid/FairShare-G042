from flask import Flask, render_template, send_file
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os

export = Flask(__name__)
