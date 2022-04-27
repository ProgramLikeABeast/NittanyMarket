import sqlite3 as sql
import pandas
import hashlib

connection = sql.connect('database.db')

users = pandas.read_csv('./data/Users.csv')
buyers = pandas.read_csv('./data/Buyers.csv')
credit_cards = pandas.read_csv('./data/Credit_Cards.csv')
address = pandas.read_csv('./data/Address.csv')
zipcode_info = pandas.read_csv('./data/Zipcode_Info.csv')
sellers = pandas.read_csv('./data/Sellers.csv')
local_vendors = pandas.read_csv('./data/Local_Vendors.csv')
categories = pandas.read_csv('./data/Categories.csv')
product_listings = pandas.read_csv('./data/Product_Listings.csv')
orders = pandas.read_csv('./data/Orders.csv')
reviews = pandas.read_csv('./data/Reviews.csv')
ratings = pandas.read_csv('./data/Ratings.csv')

user_size, buyer_size, credit_card_size, address_size = 6003, 3000, 3000, 5000
zipcode_size, seller_size, local_vendor_size, category_size = 5894, 1000, 100, 94
product_listing_size, order_size, review_size, rating_size = 699, 449, 299, 350

def encrypt(s):
    hash_obj = hashlib.sha256(bytes(s, encoding='utf-8'))
    hex_result = hash_obj.hexdigest()
    return hex_result

# filling Users Relation
for i in range(user_size):
    connection.execute('INSERT INTO Users'
                        '(email, password, e_password) '
                        'VALUES (?,?,?);',
                        (users.at[i, 'email'], users.at[i, 'password'], encrypt(users.at[i, 'password'])))

# filling Admin Relation
connection.execute('INSERT INTO Admin'
                   '(email, password)'
                   'VALUES (?,?);',
                   ('admin', encrypt('12345')))

# filling Buyers Relation
for i in range(buyer_size):
    connection.execute('INSERT INTO Buyers'
                       '(email, first_name, last_name, gender, age, home_address_id, billing_address_id) '
                       'VALUES (?,?,?,?,?,?,?);',
                       (buyers.at[i, 'email'], buyers.at[i, 'first_name'], buyers.at[i, 'last_name'], buyers.at[i, 'gender'], int(buyers.at[i, 'age']), buyers.at[i, 'home_address_id'], buyers.at[i, 'billing_address_id']))

# filling Credit_Cards Relation
for i in range(credit_card_size):
    connection.execute('INSERT INTO Credit_Cards'
                       '(credit_card_num, card_code, expire_month, expire_year, card_type, Owner_email) '
                       'VALUES (?,?,?,?,?,?);',
                       (credit_cards.at[i, 'credit_card_num'], int(credit_cards.at[i, 'card_code']), int(credit_cards.at[i, 'expire_month']), int(credit_cards.at[i, 'expire_year']), credit_cards.at[i, 'card_type'], credit_cards.at[i, 'Owner_email']))

# filling Address Relation
for i in range(address_size):
    connection.execute('INSERT INTO Address'
                        '(address_id, zipcode, street_num, street_name)'
                        'VALUES (?,?,?,?);',
                        (address.at[i, 'address_id'], int(address.at[i, 'zipcode']), int(address.at[i, 'street_num']), address.at[i, 'street_name']))

# filling in Zipcode_Info Relation
for i in range(zipcode_size):
    connection.execute('INSERT INTO Zipcode_Info'
                        '(zipcode, city, state_id, population, density, county_name, timezone) '
                        'VALUES (?,?,?,?,?,?,?);',
                        (int(zipcode_info.at[i, 'zipcode']), zipcode_info.at[i, 'city'], zipcode_info.at[i, 'state_id'], zipcode_info.at[i, 'population'], float(zipcode_info.at[i, 'density']), zipcode_info.at[i, 'county_name'], zipcode_info.at[i, 'timezone']))

# filling in Sellers Relation
for i in range(seller_size):
    connection.execute('INSERT INTO Sellers'
                        '(email, routing_number, account_number, balance)'
                        'VALUES (?,?,?,?);',
                        (sellers.at[i, 'email'], sellers.at[i, 'routing_number'], int(sellers.at[i, 'account_number']), int(sellers.at[i, 'balance'])))

# filling in the Local_Vendors Relation
for i in range(local_vendor_size):
    connection.execute('INSERT INTO Local_Vendors'
                       '(Email, Business_Name, Business_Address_ID, Customer_Service_Number)'
                       'VALUES (?,?,?,?);',
                       (local_vendors.at[i, 'Email'], local_vendors.at[i, 'Business_Name'], local_vendors.at[i, 'Business_Address_ID'], local_vendors.at[i, 'Customer_Service_Number']))
                   

# filling in Categories Relation
for i in range(category_size):
    connection.execute('INSERT INTO Categories'
                        '(parent_category, category_name) '
                        'VALUES (?,?);',
                        (categories.at[i, 'parent_category'], categories.at[i, 'category_name']))

# filling in Product_Listings Relation
for i in range(product_listing_size):
    connection.execute('INSERT INTO Product_Listings'
                       '(Seller_Email, Listing_ID, Category, Title, Product_Name, Product_Description, Price, Quantity)'
                        'VALUES (?,?,?,?,?,?,?,?);',
                        (product_listings.at[i, 'Seller_Email'], str(product_listings.at[i, 'Listing_ID']), product_listings.at[i, 'Category'], product_listings.at[i, 'Title'], product_listings.at[i, 'Product_Name'], product_listings.at[i, 'Product_Description'], product_listings.at[i, 'Price'], int(product_listings.at[i, 'Quantity'])))

# filling in Orders Relation
for i in range(order_size):
    connection.execute('INSERT INTO Orders'
                       '(Transaction_ID, Seller_Email, Listing_ID, Buyer_Email, Date, Quantity, Payment)' 
                        'VALUES (?,?,?,?,?,?,?);',
                        (str(orders.at[i, 'Transaction_ID']), orders.at[i, 'Seller_Email'], int(orders.at[i, 'Listing_ID']), orders.at[i, 'Buyer_Email'], orders.at[i, 'Date'], int(orders.at[i, 'Quantity']), int(orders.at[i, 'Payment'])))

# filling in Reviews Relation
for i in range(review_size):
    connection.execute('INSERT INTO Reviews'
                       '(Buyer_Email, Seller_Email, Listing_ID, Review_Desc) ' 
                        'VALUES (?,?,?,?);',
                        (reviews.at[i, 'Buyer_Email'], reviews.at[i, 'Seller_Email'], int(reviews.at[i, 'Listing_ID']), reviews.at[i, 'Review_Desc'],))

# filling in Ratings Relation
for i in range(rating_size):
    connection.execute('INSERT INTO Ratings'
                       '(Buyer_Email,  Seller_Email, Date, Rating, Rating_Desc)  ' 
                        'VALUES (?,?,?,?,?);',
                        (ratings.at[i, 'Buyer_Email'], ratings.at[i, 'Seller_Email'], ratings.at[i, 'Date'], int(ratings.at[i, 'Rating']), ratings.at[i, 'Rating_Desc']))

connection.commit()