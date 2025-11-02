#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    #Connect to MySQL server (no specific database yet).
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',            # change if different
            password='your_password' # update with your MySQL root password
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def create_database(connection):
    #Create ALX_prodev database if it doesn’t exist.
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev checked/created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()


def connect_to_prodev():
    #Connect directly to ALX_prodev database.
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    #Create user_data table if not exists.
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    #Insert data from CSV if not exists.
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute(
                    "SELECT COUNT(*) FROM user_data WHERE user_id = %s",
                    (row['user_id'],)
                )
                if cursor.fetchone()[0] == 0:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (row['user_id'], row['name'], row['email'], row['age'])
                    )
            connection.commit()
            print("Data inserted successfully!")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
