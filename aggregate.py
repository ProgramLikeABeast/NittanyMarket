import sqlite3 as sql

def getUniqueProductInfoFromListingId(id_list):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Product_Unique')
    connection.commit()
    tempList = []
    for id in id_list:
        result = cursor.execute('SELECT DISTINCT Title, Product_Name, Product_Description, Listing_ID FROM Product_Listings WHERE Listing_ID=?;', (id, ))
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
    info = getUniqueProductInfoFromListingId([lid])[0]
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
