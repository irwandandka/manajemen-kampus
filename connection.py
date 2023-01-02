from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'polibatamkw'
mysql = MySQL(app)

# APP secret key (bebas)
app.secret_key = "4cc645e832bc2ed0869da6d3a9bdc0ea"