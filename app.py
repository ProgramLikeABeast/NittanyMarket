from flask import Flask, render_template, request, make_response
import sqlite3 as sql
import hashlib
import time

from Category import Category
from aggregate import *

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
            response =  make_response(render_template('dashboard.html', info=infoPackUp(email)))
            response.set_cookie('email', email)
            return response
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
        email = request.cookies.get('email')
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category="Root";')
        return render_template('./category/category.html', result=result, info=infoPackUp(email))
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
        email = request.cookies.get('email')
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category=?;', (category, ))
        return render_template('./category/category_2.html', result=result, info=infoPackUp(email))

@app.route('/category_3', methods=['POST', 'GET'])
def category_3():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if request.method == 'GET':
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category="Root";')
        return render_template('./category/category_3.html', result=result)
    if request.method == 'POST':
        category = request.form['category']
        email = request.cookies.get('email')
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category=?;', (category, ))
        return render_template('./category/category_3.html', result=result, info=infoPackUp(email))

@app.route('/category_4', methods=['POST', 'GET'])
def category_4():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if request.method == 'GET':
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category="Root";')
        return render_template('./category/category_4.html', result=result)
    if request.method == 'POST':
        category = request.form['category']
        email = request.cookies.get('email')
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category=?;', (category, ))
        return render_template('./category/category_4.html', result=result, info=infoPackUp(email))

@app.route('/product_list', methods=['POST', 'GET'])
def product_list():
    if request.method == 'POST':
        category = request.form['category']
        email = request.cookies.get('email')
        result = getUniqueProductInfoFromListingId(Category(category).getListingIds())
        return render_template('product_list.html', result=result, info=infoPackUp(email))

@app.route('/product', methods=['POST', 'GET'])
def product_detail():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if request.method == 'POST':
        lid = request.form['lid']
        email = request.cookies.get('email')
        query_result = cursor.execute('SELECT DISTINCT * FROM Product_Listings WHERE Listing_ID=?;', (lid, ))
        product_info = [row for row in query_result]
        product_review = getReviewInfoFromSingleListingId(lid)
        return render_template('product.html', product=[product_info, product_review], info=infoPackUp(email))

@app.route('/seller_list', methods=['POST', 'GET'])
def seller_list():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    email = request.cookies.get('email')
    result = []
    query_result = cursor.execute('SELECT DISTINCT email FROM Sellers;')
    for row in query_result:
        result.append(row[0].replace("('", "".replace("',)", "")))
    return render_template('seller_list.html', result=result, info=infoPackUp(email))

@app.route('/seller', methods=['POST', 'GET'])
def seller():
    if request.method == 'POST':
        seller_email = request.form['seller_email']
        email = request.cookies.get('email')
        return render_template('seller.html', seller_email=seller_email, info=infoPackUp(email), product_list=getProductsFromSellerEmail(seller_email), rating_list=getRatingsFromSellerEmail(seller_email))

@app.route('/order', methods=['POST', 'GET'])
def order():
    email = request.cookies.get('email')
    order_and_product = getOrderProductInfoFromBuyerEmail(email)
    return render_template('order.html', order_and_product=order_and_product, info=infoPackUp(email))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    email = request.cookies.get('email')
    buyer, seller = [], []
    if isBuyer(email):
        buyer = getBuyerAddressZipcodeFromEmail(email)
    if isSeller(email):
        seller = getSellerFromEmail(email)
    credit_card = getCreditCardFromEmail(email)
    return render_template('profile.html', buyer=buyer, seller=seller, credit_card=credit_card, info=infoPackUp(email))


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

def infoPackUp(email):
    info = [email]
    info.append(isBuyer(email))
    info.append(isSeller(email))
    info.append(isAdmin(email))
    info.append(isLocalVendor(email))
    return info

def isAdmin(email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Admin WHERE email=?;", (email, ))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True

def isSeller(email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Sellers WHERE email=?;", (email, ))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True

def isBuyer(email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Buyers WHERE email=?;", (email, ))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True

def isLocalVendor(email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Local_Vendors WHERE email=?;", (email, ))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True
