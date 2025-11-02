import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    
    # Generator that fetches users from the database in batches. Yields one batch (list of rows) at a time.
   
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',               # adjust as needed
            password='your_password',  # update your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user_data;")

            batch = []
            for row in cursor:
                batch.append(row)
                if len(batch) == batch_size:
                    yield batch  # yield a full batch
                    batch = []   # reset batch

            # yield any remaining rows
            if batch:
                yield batch

    except Error as e:
        print(f"Database error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def batch_processing(batch_size=5):
    
    # Processes each batch from stream_users_in_batches and filters users over age 25.
    
    for batch in stream_users_in_batches(batch_size):  # loop 1
        filtered = [user for user in batch if float(user[3]) > 25]  # loop 2 (list comp)
        yield filtered  # yield the filtered batch