import sqlite3 as sql

connection = sql.connect('database.db')

connection.execute('DROP TABLE IF EXISTS Users')
connection.execute('DROP TABLE IF EXISTS Admin')
connection.execute('DROP TABLE IF EXISTS Buyers')
connection.execute('DROP TABLE IF EXISTS Credit_Cards')
connection.execute('DROP TABLE IF EXISTS Zipcode_Info')
connection.execute('DROP TABLE IF EXISTS Address')
connection.execute('DROP TABLE IF EXISTS Sellers')
connection.execute('DROP TABLE IF EXISTS Local_Vendors')
connection.execute('DROP TABLE IF EXISTS Categories')
connection.execute('DROP TABLE IF EXISTS Product_Listings')
connection.execute('DROP TABLE IF EXISTS Orders')
connection.execute('DROP TABLE IF EXISTS Reviews')
connection.execute('DROP TABLE IF EXISTS Ratings')
# extra databases
connection.execute('DROP TABLE IF EXISTS Product_Unique')


connection.commit()

connection.execute('CREATE TABLE Users('
                   'email STRING UNIQUE,'
                   'password STRING,'
                   'e_password STRING);')

connection.execute('CREATE TABLE Admin('
                   'email STRING UNIQUE,'
                   'password STRING);')

connection.execute('CREATE TABLE Buyers('
                   'email STRING UNIQUE,'
                   'first_name STRING,'
                   'last_name STRING,'
                   'gender STRING,'
                   'age INTEGER,'
                   'home_address_id STRING,'
                   'billing_address_id STRING);')

connection.execute('CREATE TABLE Credit_Cards('
                   'credit_card_num STRING UNIQUE,'
                   'card_code INTEGER,'
                   'expire_month INTEGER,'
                   'expire_year INTEGER,'
                   'card_type STRING,'
                   'Owner_email STRING);')

connection.execute('CREATE TABLE Address('
                   'address_id STRING UNIQUE,'
                   'zipcode INTEGER,'
                   'street_num INTEGER,'
                   'street_name STRING);')

connection.execute('CREATE TABLE Zipcode_Info('
                   'zipcode INTEGER,'
                   'city STRING,'
                   'state_id STRING,'
                   'population INTEGER,'
                   'density REAL,'
                   'county_name STRING,'
                   'timezone STRING);')

connection.execute('CREATE TABLE Sellers('
                   'email STRING UNIQUE,'
                   'routing_number STRING,'
                   'account_number INTEGER,'
                   'balance REAL);')

connection.execute('CREATE TABLE Local_Vendors('
                   'Email STRING UNIQUE,'
                   'Business_Name STRING,'
                   'Business_Address_ID STRING,'
                   'Customer_Service_Number STRING);')

connection.execute('CREATE TABLE Categories('
                   'parent_category STRING,'
                   'category_name STRING UNIQUE);')

connection.execute('CREATE TABLE Product_Listings('
                   'Seller_Email STRING,'
                   'Listing_ID INTEGER,'
                   'Category STRING,'
                   'Title STRING,'
                   'Product_Name STRING,'
                   'Product_Description STRING,'
                   'Price STRING,'
                   'Quantity INTEGER);')
# 'UNIQUE(Seller_Email, Listing_ID));')

connection.execute('CREATE TABLE Orders('
                   'Transaction_ID INTEGER UNIQUE,'
                   'Seller_Email STRING,'
                   'Listing_ID INTEGER,'
                   'Buyer_Email STRING,'
                   'Date DATE,'
                   'Quantity INTEGER,'
                   'Payment INTEGER);')

connection.execute('CREATE TABLE Reviews('
                   'Buyer_Email STRING,'
                   'Seller_Email STRING,'
                   'Listing_ID INTEGER,'
                   'Review_Desc STRING,'
                   'UNIQUE(Buyer_Email, Seller_Email, Listing_ID));')

connection.execute('CREATE TABLE Ratings('
                   'Buyer_Email STRING,'
                   'Seller_Email STRING,'
                   'Date DATE,'
                   'Rating INTEGER,'
                   'Rating_Desc STRING,'
                   'UNIQUE(Buyer_Email, Seller_Email, Date));')

connection.execute('CREATE TABLE Product_Unique('
                   'Title STRING,'
                   'Product_Name STRING,'
                   'Product_Description STRING,'
                   'Listing_ID INTEGER,'
                   'UNIQUE(Title, Product_Name, Product_Description));')

connection.commit()
