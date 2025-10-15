import pyodbc

class DatabaseConnection:
    def __init__(self):
        self.server = ''
        self.database = 'GYM'
        self.username = ''
        self.password = 'pola'
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            conn_str = (
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER=DESKTOP-D577I1V\\SQLEXPRESS;'
                f'DATABASE=GYM;'
                f'UID=pola;'
                f'PWD=pola;'
            )
            self.connection = pyodbc.connect(conn_str)
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            print(" Connection failed:", e)

    def close(self):
        if self.conn:
            self.conn.close()
            print("🔒 Connection closed.")

if __name__ == '__main__':
    db = DatabaseConnection()  
    db.connect()               
    db.close()                 
