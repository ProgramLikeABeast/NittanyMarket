import sqlite3 as sql

class Category:
    def __init__(self, category):
        self.category = category
        self.product_id_list = []
        self.searchedCategories = {self.category:True}
        self.cursor = sql.connect('database.db').cursor()

    def searchOneLayer(self, category):
        queryResult = self.cursor.execute('SELECT DISTINCT category_name FROM Categories WHERE parent_category=?;', (category, ))
        result = [row[0].replace('(', "").replace("',)", "") for row in queryResult]
        return [category] + result

    def search(self, currCategory = None):
        if currCategory == None:
            currCategory = self.category
        queryResult = self.searchOneLayer(currCategory)
        for row in queryResult:
            if row not in self.searchedCategories:
                self.searchedCategories[row] = True
                self.search(row)
    
    def search_test(self):
        self.searchedCategories = {self.category:True}
        self.search(self.category)
        return self.searchedCategories

    def getListingIds(self):
        self.searchedCategories = {self.category:True}
        self.product_id_list = []
        self.search()
        for category in self.searchedCategories:
            queryResult = self.cursor.execute('SELECT DISTINCT Listing_ID FROM Product_Listings WHERE Category=?;', (category, ))
            for row in queryResult:
                self.product_id_list.append(row[0])
        self.product_id_list = list(set(self.product_id_list))
        return self.product_id_list
        
