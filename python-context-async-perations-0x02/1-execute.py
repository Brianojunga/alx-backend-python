import sqlite3


class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()
    
    def __exit__(self, type, value, traceback):
        if type:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()

# Example executation
with ExecuteQuery('example.db', 'SELECT * FROM users WHERE age > ?', 25) as results:
    for row in results:
        print(row)