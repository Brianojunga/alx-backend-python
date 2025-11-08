import time
import sqlite3 
import functools


query_cache = {}

"""your code goes here"""
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

def cache_query(func):
    @functools.wraps(func)
    def wrapper(connection, query, *args, **kwargs):
        try:
            if query in query_cache:
                return query_cache[query]
            result = func(connection, query, *args, **kwargs)
            query_cache[query] = result
            return result
        except Exception as e:
            raise e
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")