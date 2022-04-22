from flask import Flask, render_template, request
import sqlite3 as sql
import hashlib
import time

from Category import Category
from aggregate import getUniqueProductInfoFromListingId, getReviewInfoFromSingleListingId

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('adminDashboard.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == 'POST':
        email, password = request.form['email'], request.form['password']
        # if the user is found in User Relation, go to dashboard page
        if loginVerify(email, password):
            return render_template('dashboard.html', isAdmin=adminVerify(email, password))
        # if the email password tuple doesn't exist, go to loginError page
        else:
            return render_template('loginError.html')
    if request.method == 'GET':
        return render_template('loginError.html')

@app.route('/user', methods=['POST', 'GET'])
def user():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    result = cursor.execute('SELECT * FROM users;')
    return render_template('user.html', result=result)

@app.route('/category', methods=['POST', 'GET'])
def category():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if request.method == 'GET':
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category="Root";')
        return render_template('./category/category.html', result=result)
    if request.method == 'POST':
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category="Root";')
        return render_template('./category/category.html', result=result)

@app.route('/category_2', methods=['POST', 'GET'])
def category_2():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if request.method == 'GET':
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category="Root";')
        return render_template('./category/category_2.html', result=result)
    if request.method == 'POST':
        category = request.form['category']
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category=?;', (category, ))
        return render_template('./category/category_2.html', result=result, category=category)

@app.route('/category_3', methods=['POST', 'GET'])
def category_3():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if request.method == 'GET':
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category="Root";')
        return render_template('./category/category_3.html', result=result)
    if request.method == 'POST':
        category = request.form['category']
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category=?;', (category, ))
        return render_template('./category/category_3.html', result=result, category=category)

@app.route('/category_4', methods=['POST', 'GET'])
def category_4():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if request.method == 'GET':
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category="Root";')
        return render_template('./category/category_4.html', result=result)
    if request.method == 'POST':
        category = request.form['category']
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category=?;', (category, ))
        return render_template('./category/category_4.html', result=result, category=category)

@app.route('/product_list', methods=['POST', 'GET'])
def product_list():
    if request.method == 'POST':
        category = request.form['category']
        result = getUniqueProductInfoFromListingId(Category(category).getListingIds())
        return render_template('product_list.html', result=result)

@app.route('/product', methods=['POST', 'GET'])
def product_detail():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if request.method == 'POST':
        lid = request.form['lid']
        query_result = cursor.execute('SELECT DISTINCT * FROM Product_Listings WHERE Listing_ID=?;', (lid, ))
        product_info = [row for row in query_result]
        product_review = getReviewInfoFromSingleListingId(lid)
        return render_template('product.html', product=[product_info, product_review])

def encrypt(s):
    hash_obj = hashlib.sha256(bytes(s, encoding='utf-8'))
    hex_result = hash_obj.hexdigest()
    return hex_result

def loginVerify(email, password):
    e_password = encrypt(password)
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE email=? AND e_password=?;", (email, e_password))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True

def adminVerify(email, passowrd):
    e_password = encrypt(passowrd)
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Admin WHERE email=? AND password=?;", (email, e_password))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True

