import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    """ your code goes here""" 
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('users.db')
        try:
            result = func(connection, *args, **kwargs)
            return result
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise
        finally:
            connection.close()

    return wrapper

""" your code goes here"""
def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(connection, *args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    results = func(connection, *args, **kwargs)
                    return results
                except Exception as e:
                    attempts += 1
                    print(f"Attempt : {attempts + 1}, Error : {e}")
                    time.sleep(delay)
            raise Exception(f'Failed to connect after {retries} attempts')
        
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)