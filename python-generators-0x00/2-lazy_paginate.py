#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database
    using LIMIT and OFFSET.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',               # change if needed
            password='my_password',  # my MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset};"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    except Error as e:
        print(f"Database error: {e}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def lazy_paginate(page_size):
    """
    Generator that lazily fetches pages from the database.
    Loads the next page only when needed.
    Uses only one loop.
    """
    offset = 0
    while True:  # single loop
        page = paginate_users(page_size, offset)
        if not page:   # stop when no more rows
            break
        yield page
        offset += page_size
