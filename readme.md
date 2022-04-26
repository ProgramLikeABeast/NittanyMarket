# NittanyMarket

## Set Up
### 1. Database Setup
initialize database and create tables
```python
python dbCreation.py
```
inject artificial data into the tables
```python
python dbPopulation.py
```
### 2. Put Up Server(for window users)
activate venv environment
```bash
venv\Scripts\activate
```
start flask server
```bash
flask run
```
## Project Overview
### 1. Technical Stacks
- HTML for webpages(non-SPA), Bootstrap 4 for stylesheet and JavaScript and JQuery for simple page actions
- Flask framework and Python3 for backend; Flask provides routing of pages which are associated with view functions that conditionally renders pages with operational results, makes use of form and cookies in the HTTP request methods (GET, POST) to do queries in the database
- Sqlite3 for local database; used connection and cursor objects to execute SQL CRUD operations with multiple relations.
- Jinja template engine is used in HTML page to achieve data embedding into page in the form of semi-separation between frontend and backend.
### 2. Basic Functions
NittanyMarket supports the hierarchy of different types of users. Different types of users accesses different functionalities and some high-level users are able to access more other than basic ones.
- Users: the basic level users, can access Category List, Seller List and Personal Profile; they cannot buy nor sell.
- Buyers: other than basic accesses of users, buyers can order stuff to the seller to be confirmed and cancel orders; they can also access to the Buyer Orders to check order history.
- Sellers: other than basic accesses of users, sellers confirme or refuse orders; they can also access to the Seller Orders to check order history; they can create new categories and product listings to be checked by admins.
- Local Vendors: they are ordinary users until approved to be sellers by admin.
- Admin: they are the highest-level users, who can mmanage the categories, approve local vendors to be sellers and approve revocation of past orders.
Here are some basic description of the functionalities.
- Login status: when login, your user status will be recorded by cookies and remembered throughout the session.
- Category: category hierarchy is implemented and from a parent category the child category products are available. Users can select from any level of categories and see the product lists associated. From selected product page, users can still switch to categories and seller page associated with the product.
- Sellers: all the sellers registered and their products and ratings received.
- Buyer Orders: all the past orders made by the buyer and pending orders to be confirmed by the sellers.
- Seller Orders: all the past orders confirmed by the seller and pending orders to be confirmed or refused.
- Profile: user information display, including card types and addresses; for local vendors, they can apply to change their status to be sellers.
