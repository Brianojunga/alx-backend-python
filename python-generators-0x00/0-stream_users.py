import mysql.connector
from mysql.connector import Error


def stream_users():
   
    #Generator that streams rows from user_data table one by one.Uses only one loop and yield to return each row.

    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',              # change as needed
            password='your_password', # change as needed
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user_data;")

            # Stream rows using a generator (one loop only)
            for row in cursor:
                yield row

    except Error as e:
        print(f"Database error: {e}")

    finally:
        # Close connection after generator is exhausted
        if connection.is_connected():
            cursor.close()
            connection.close()
