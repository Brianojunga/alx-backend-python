import sqlite3


class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self,type, value, traceback):
        if type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()
        self.cursor.close()

#example usage
with DatabaseConnection('example.db') as cursor:
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
