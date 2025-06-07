# database.py
import sqlite3
import datetime

class DatabaseManager:
    def __init__(self, db_name='marcenaria.db'):
        """Conecta ao banco de dados ao ser instanciada."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Cria as tabelas do sistema se elas não existirem."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY, password TEXT NOT NULL)
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
                description TEXT, price REAL NOT NULL)
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT NOT NULL,
                order_date TEXT NOT NULL, status TEXT NOT NULL, total REAL NOT NULL)
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER,
                product_id INTEGER, quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id))
        ''')
        self.conn.commit()

    # --- MÉTODOS DE USUÁRIO ---
    def check_user_exists(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()

    def add_user(self, username, password):
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"DB Error on add_user: {e}")
            return False

    def verify_user(self, username, password):
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        return self.cursor.fetchone()

    # --- MÉTODOS DE PRODUTO ---
    def add_product(self, name, description, price):
        try:
            self.cursor.execute('INSERT INTO products (name, description, price) VALUES (?, ?, ?)', (name, description, float(price)))
            self.conn.commit()
            return True
        except (sqlite3.Error, ValueError) as e:
            print(f"DB Error on add_product: {e}")
            return False

    def get_all_products(self):
        self.cursor.execute('SELECT id, name, description, price FROM products')
        return self.cursor.fetchall()

    def get_product(self, prod_id):
        self.cursor.execute('SELECT name, description, price FROM products WHERE id = ?', (prod_id,))
        return self.cursor.fetchone()

    def update_product(self, prod_id, name, desc, price):
        try:
            self.cursor.execute('UPDATE products SET name=?, description=?, price=? WHERE id=?', (name, desc, float(price), prod_id))
            self.conn.commit()
            return True
        except (sqlite3.Error, ValueError) as e:
            print(f"DB Error on update_product: {e}")
            return False

    def delete_product(self, prod_id):
        try:
            self.cursor.execute('DELETE FROM products WHERE id = ?', (prod_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"DB Error on delete_product: {e}")
            return False

    # --- MÉTODOS DE ENCOMENDA ---
    def create_order(self, client_name, order_total, items):
        try:
            current_date = datetime.date.today().isoformat()
            self.cursor.execute('INSERT INTO orders (client_name, order_date, status, total) VALUES (?, ?, ?, ?)',
                               (client_name, current_date, 'Pendente', order_total))
            order_id = self.cursor.lastrowid
            for item in items:
                self.cursor.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)',
                                   (order_id, item['id'], item['quantity']))
            self.conn.commit()
            return order_id
        except sqlite3.Error as e:
            print(f"DB Error on create_order: {e}")
            return None

    def get_order_status(self, order_id):
        self.cursor.execute('SELECT status FROM orders WHERE id = ?', (order_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_order_status(self, order_id, new_status):
        self.cursor.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_full_report(self):
        self.cursor.execute('SELECT id, client_name, order_date, status, total FROM orders ORDER BY id DESC')
        orders = self.cursor.fetchall()
        report_data = []
        for order in orders:
            order_id = order[0]
            self.cursor.execute('''
                SELECT p.name, oi.quantity
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = ?
            ''', (order_id,))
            items = self.cursor.fetchall()
            report_data.append({'order': order, 'items': items})
        return report_data
    
    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()