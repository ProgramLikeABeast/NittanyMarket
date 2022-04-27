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
        return render_template('login_error.html')

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
        email = request.cookies.get('email')
        category = request.form['category']
        result = cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category=?;', (category, ))
        return render_template('./category/category.html', result=result, info=infoPackUp(email))

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
        seller = getSellerFromListingId(lid)
        return render_template('product.html', product_info=product_info, seller=seller, product_review=product_review
        , info=infoPackUp(email))

@app.route('/transaction', methods=['POST', 'GET'])
def product_transaction():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if request.method == 'POST':
        lid = request.form['lid']
        email = request.cookies.get('email')
        query_result = cursor.execute('SELECT DISTINCT * FROM Product_Listings WHERE Listing_ID=?;', (lid, ))
        product_info = [row for row in query_result]
        product_review = getReviewFromListingId(lid)
        return render_template('product_transaction.html', product_info=product_info, product_review=product_review
        , info=infoPackUp(email))

@app.route('/message', methods=['POST', 'GET'])
def message():
    time.sleep(2)
    email = request.cookies.get('email')
    quantity = int(request.form['quantity'])
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if quantity > 0:
        lid = request.form['lid']
        seller_email = request.form['seller_email']
        price = int(request.form['price'].replace("$", "").replace(",", ""))
        createPendingOrder(email, seller_email, lid, quantity, price)
    # buyer cancels order/seller refuses the order
    elif quantity == -2 or quantity == -3:
        tid = request.form['tid']
        cursor.execute('DELETE FROM Pending_Orders WHERE Transaction_ID=?', (tid, ))
    # seller refuses order
    elif quantity == -4:
        tid = request.form['tid']
        result = cursor.execute('SELECT * FROM Pending_Orders WHERE Transaction_ID=?', (tid, ))
        for row in result:
            cursor.execute('INSERT INTO Orders(Transaction_ID,Seller_Email,Listing_ID,Buyer_Email,Date,Quantity,Payment) VALUES(?,?,?,?,?,?,?);', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], ))
            cursor.execute('UPDATE Product_Listings SET Quantity = Quantity-? WHERE Listing_ID=?', (row[5], row[2], ))
            cursor.execute('UPDATE Sellers SET balance = balance + ? WHERE email=?', (row[6], row[1], ))
        cursor.execute('DELETE FROM Pending_Orders WHERE Transaction_ID=?', (tid, ))
    elif quantity == -5:
        lid = encrypt(str(time.time()))
        Category, Title, Product_Name, Product_Description, Price, Quantity, Active_Until = request.form['category'], request.form['title'], request.form['name'], request.form['description'], '$'+request.form['price'], int(request.form['number']), request.form['active_until']
        if not isCategory(Category):
            connection.commit()
            cursor.close()
            return render_template('message.html', quantity=-6, info=infoPackUp(email))
        cursor.execute('INSERT INTO Product_Listings (Seller_Email,Listing_ID,Category,Title,Product_Name,Product_Description,Price,Quantity) VALUES(?,?,?,?,?,?,?,?);', (email, lid, Category, Title, Product_Name, Product_Description, Price, Quantity))
        cursor.execute('INSERT INTO Active (Listing_ID, Active_Until) VALUES(?,?);', (lid, Active_Until))
    connection.commit()
    cursor.close()
    return render_template('message.html', quantity=quantity, info=infoPackUp(email))

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

@app.route('/buyer_order', methods=['POST', 'GET'])
def buyer_order():
    email = request.cookies.get('email')
    buyer_order_and_product = getOrderProductInfoFromBuyerEmail(email)
    pending_buyer_order_and_product = getPendingOrderProductInfoFromBuyerEmail(email)
    return render_template('buyer_order.html', buyer_order_and_product=buyer_order_and_product, pending_buyer_order_and_product=pending_buyer_order_and_product, info=infoPackUp(email))

@app.route('/seller_order', methods=['GET', 'POST'])
def seller_order():
    email = request.cookies.get('email')
    seller_order_and_product = getOrderProductInfoFromSellerEmail(email)
    pending_seller_order_and_product = getPendingOrderProductInfoFromSellerEmail(email)
    return render_template('seller_order.html', seller_order_and_product=seller_order_and_product, pending_seller_order_and_product=pending_seller_order_and_product, info=infoPackUp(email))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    email = request.cookies.get('email')
    buyer, seller, local_vendor, address = [], [], [], []
    if isBuyer(email):
        buyer = getBuyerAddressZipcodeFromEmail(email)
    if isSeller(email):
        seller = getSellerFromEmail(email)
    if isLocalVendor(email):
        local_vendor = getLocalVendorFromEmail(email)
        address = getAddressZipcodeFromAddressId(local_vendor[0][2])
    credit_card = getCreditCardFromEmail(email)
    return render_template('profile.html', buyer=buyer, seller=seller, local_vendor=local_vendor, address=address, credit_card=credit_card, info=infoPackUp(email))

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    email = request.cookies.get('email')
    return render_template('publish_product.html', info=infoPackUp(email))

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

def isCategory(category):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Categories WHERE parent_category=? OR category_name=?;", (category,category ))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True
