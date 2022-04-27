import sqlite3 as sql
from datetime import date
import hashlib
import time

def getUniqueProductInfoFromListingId(id_list):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Product_Unique')
    connection.commit()
    tempList = []
    for id in id_list:
        result = cursor.execute('SELECT DISTINCT Title, Product_Name, Product_Description, Listing_ID FROM Product_Listings WHERE Listing_ID=? AND Quantity>0;', (id, ))
        # decompose query result
        for row in result:
           tempList.append(row)
    insertIntoProductUnique(tempList)
    result = cursor.execute('SELECT * FROM Product_Unique;')
    retList = [row for row in result]
    cursor.close()
    return retList

def insertIntoProductUnique(infoList):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    for info in infoList:
        try:
            cursor.execute('INSERT INTO Product_Unique(Title, Product_Name, Product_Description, Listing_ID) VALUES (?, ?, ?, ?);', (info[0], info[1], info[2], info[3]))
        except:
            continue
    connection.commit()
    cursor.close()

def getListingIdListFromSingleListingId(lid):
    productInfo = getUniqueProductInfoFromListingId([lid])
    if not productInfo:
        return []
    info = productInfo[0]
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    result = cursor.execute('SELECT Listing_ID FROM Product_Listings WHERE Title=? AND Product_Name=? AND Product_Description=?;', (info[0], info[1], info[2]))
    retList = [row[0] for row in result]
    cursor.close()
    return retList

def getReviewInfoFromSingleListingId(lid):
    lidList = getListingIdListFromSingleListingId(lid)
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    for listing_id in lidList:
        result = cursor.execute('SELECT * FROM Reviews WHERE Listing_ID=?', (listing_id, ))
        if result is not None:
            for row in result:
                retList.append(row)
    cursor.close()
    return retList

def getProductsFromSellerEmail(email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    result = cursor.execute('SELECT DISTINCT * FROM Product_Listings WHERE Seller_Email=?;', (email, ))
    for row in result:
        retList.append(row)
    return retList

def getRatingsFromSellerEmail(email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    result = cursor.execute('SELECT DISTINCT * FROM Ratings WHERE Seller_Email=?;', (email, ))
    for row in result:
        retList.append(row)
    cursor.close()
    return retList

def getPendingOrderProductInfoFromBuyerEmail(buyer_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    tempList = []
    result = cursor.execute('SELECT DISTINCT * FROM Pending_Orders WHERE Buyer_Email=?;', (buyer_email, ))
    for row in result:
        tempList.append(row)
    for row in tempList:
        listing_id = row[2]
        result2 = cursor.execute('SELECT DISTINCT Title, Product_Name FROM Product_Listings WHERE Listing_ID=?;', (listing_id, ))
        for row2 in result2:
            row += row2
        retList.append(row)
    cursor.close()
    return retList

def getOrderProductInfoFromBuyerEmail(buyer_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    tempList = []
    result = cursor.execute('SELECT DISTINCT * FROM Orders WHERE Buyer_Email=?;', (buyer_email, ))
    for row in result:
        tempList.append(row)
    for row in tempList:
        listing_id = row[2]
        result2 = cursor.execute('SELECT DISTINCT Title, Product_Name FROM Product_Listings WHERE Listing_ID=?;', (listing_id, ))
        for row2 in result2:
            row += row2
        retList.append(row)
    cursor.close()
    return retList

def getPendingOrderProductInfoFromSellerEmail(seller_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    tempList = []
    result = cursor.execute('SELECT DISTINCT * FROM Pending_Orders WHERE Seller_Email=?;', (seller_email, ))
    for row in result:
        tempList.append(row)
    for row in tempList:
        listing_id = row[2]
        result2 = cursor.execute('SELECT DISTINCT Title, Product_Name FROM Product_Listings WHERE Listing_ID=?;', (listing_id, ))
        for row2 in result2:
            row += row2
        retList.append(row)
    cursor.close()
    return retList

def getOrderProductInfoFromSellerEmail(seller_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    tempList = []
    result = cursor.execute('SELECT DISTINCT * FROM Orders WHERE Seller_Email=?;', (seller_email, ))
    for row in result:
        tempList.append(row)
    for row in tempList:
        listing_id = row[2]
        result2 = cursor.execute('SELECT DISTINCT Title, Product_Name FROM Product_Listings WHERE Listing_ID=?;', (listing_id, ))
        for row2 in result2:
            row += row2
        retList.append(row)
    cursor.close()
    return retList

def getBuyerFromEmail(buyer_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    result = cursor.execute('SELECT DISTINCT * FROM Buyers WHERE email=?;', (buyer_email, ))
    for row in result:
        retList.append(row)
    cursor.close()
    return retList, retList[0][5]

def getSellerFromEmail(seller_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    result = cursor.execute('SELECT DISTINCT * FROM Sellers WHERE email=?;', (seller_email, ))
    for row in result:
        retList.append(row)
    cursor.close()
    return retList

def getAddressFromAddressId(address_id):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    result = cursor.execute('SELECT DISTINCT * FROM Address WHERE address_id=?;', (address_id, ))
    for row in result:
        retList.append(row)
    cursor.close()
    return retList, retList[0][1]

def getZipcodeInfoFromZipcode(zipcode):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    result = cursor.execute('SELECT DISTINCT * FROM Zipcode_Info WHERE zipcode=?;', (zipcode, ))
    for row in result:
        retList.append(row)
    cursor.close()
    return retList

def getAddressZipcodeFromAddressId(aid):
    address, zipcode = getAddressFromAddressId(aid)
    zipcode_info = getZipcodeInfoFromZipcode(zipcode)
    address[0] += zipcode_info[0]
    return address

def getBuyerAddressZipcodeFromEmail(email):
    buyer, address_id = getBuyerFromEmail(email)
    address, zipcode = getAddressFromAddressId(address_id)
    zipcode_info = getZipcodeInfoFromZipcode(zipcode)
    buyer[0] += address[0]
    buyer[0] += zipcode_info[0]
    return buyer

def getCreditCardFromEmail(email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    result = cursor.execute('SELECT DISTINCT * FROM Credit_Cards WHERE Owner_email=?;', (email, ))
    for row in result:
        retList.append(row)
    cursor.close()
    return retList

def getProductInfoFromListingId(lid):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    result = cursor.execute('SELECT DISTINCT Title,Product_Name,Product_Description FROM Product_Listings WHERE Listing_ID=?;', (lid, ))
    for row in result:
        retList.append(row)
    cursor.close()
    return retList

def getSellerFromListingId(lid):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    title, productName, productDescription = getProductInfoFromListingId(lid)[0]
    retList = []
    result = cursor.execute('SELECT Seller_Email, Price, Quantity, Listing_ID FROM Product_Listings WHERE Title=? AND Product_Name=? AND Product_Description=? AND Quantity>0;', (title, productName, productDescription, ))
    for row in result:
        retList.append(row)
    cursor.close()
    return retList

def getReviewFromListingId(lid):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    result = cursor.execute('SELECT Buyer_Email, Review_Desc FROM Reviews WHERE Listing_ID=?;', (lid, ))
    for row in result:
        retList.append(row)
    cursor.close()
    return retList

def getLocalVendorFromEmail(email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    retList = []
    result = cursor.execute('SELECT * FROM Local_Vendors WHERE Email=?;', (email, ))
    for row in result:
        retList.append(row)
    cursor.close()
    return retList

def encrypt(s):
    hash_obj = hashlib.sha256(bytes(s, encoding='utf-8'))
    hex_result = hash_obj.hexdigest()
    return hex_result

def createPendingOrder(email, seller_email, lid, quantity, price):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Pending_Orders'
                   '(Transaction_ID, Seller_Email, Listing_ID, Buyer_Email, Date, Quantity, Payment)' 
                   'VALUES (?,?,?,?,?,?,?);',
                    (encrypt(str(time.time())), seller_email, lid, email, date.today().strftime("%m/%d/%y"), quantity, quantity*price))
    connection.commit()
    cursor.close()
    