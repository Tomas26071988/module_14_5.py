import sqlite3


def initiate_product_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # создаю таблицу продуктов
    cursor.execute('''
    
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL)
    ''')

    conn.commit()
    conn.close()

def initiate_users_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()


    cursor.execute('''
        
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INT NOT NULL,
            balance INT NOT NULL)
    ''')

    conn.commit()
    conn.close()


def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    conn.close()
    return products


def add_product(title, description, price):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Products(title, description, price) VALUES(?, ?, ?)
    ''', (title, description, price))

    conn.commit()
    conn.close()


def add_user(username, email, age):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Добавление нового пользователя с балансом 1000
    cursor.execute('''
    INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, 1000)
    ''', (username, email, age))

    conn.commit()
    conn.close()


def is_included(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM Users WHERE username = ?', (username,))
    user_exists = cursor.fetchone() is not None
    conn.close()
    return user_exists

