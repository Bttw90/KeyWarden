import sqlite3

class Database():
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(f'{self.db_name}.db')
            self.cursor = self.connection.cursor()
            print('Successful connection to the database.')
        except sqlite3.Error as e:
            print(f'Error while connecting to the database: {e}')

    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print('Database connection closed successfully.')
            self.connection = None


    def create_users_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, user_name VARCHAR(50) NOT NULL UNIQUE, hashed_master_key VARCHAR(60) NOT NULL, salt VARCHAR(60) NOT NULL)')
        
    
    def create_user_psw_table(self, user_name):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {user_name} (login_name VARCHAR(50) NOT NULL UNIQUE, password VARBINARY(255) NOT NULL, app_name VARCHAR(50) NOT NULL UNIQUE)')


    def insert_user_table(self, user_name, hashed_master_key, salt):
        try:
            self.cursor.execute('INSERT INTO users (user_name, hashed_master_key, salt) VALUES (?, ?, ?)', (user_name, hashed_master_key, salt))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f'Error while inserting data: {e}')
            return False


    def insert_psw_table(self, user_name, login_name, app_name, password):
        try:
            self.cursor.execute(f'INSERT INTO {user_name} (login_name, password, app_name) VALUES (?, ?, ?)', (login_name, password, app_name))
            self.connection.commit()
        except Exception as e:
            print(f'Error while inserting data: {e}')


    def get_master_psw(self, user_name):
        try:
            self.cursor.execute('SELECT hashed_master_key FROM users WHERE user_name = ?', (user_name,))
            db_hashed_psw = self.cursor.fetchone()
            if db_hashed_psw:
                hashed_psw = db_hashed_psw[0]
                print('Data retrieved')
                return hashed_psw
            else:
                print('No data found associated to user_name = ', user_name)
        except  Exception as e:
            print(f'Error while inserting data: {e}')

    
    def get_salt(self, user_name):
        try:
            self.cursor.execute('SELECT salt FROM users WHERE user_name = ?', (user_name,))
            db_salt = self.cursor.fetchone()
            if db_salt:
                salt = db_salt[0]
                print('Salt retrieved')
                return salt
            else:
                print('No salt found associated to user_name = ', user_name)
        except Exception as e:
            print(f'Error while retrieving data: {e}')