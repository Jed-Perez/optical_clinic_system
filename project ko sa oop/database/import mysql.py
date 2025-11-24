import mysql.connector
from mysql.connector import Error
import logging
from .db_config import DB_CONFIG  

logging.basicConfig(level=logging.INFO)

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                logging.info(" Connected to database.")
        except Error as e:
            logging.error(" DB connection error: %s", e)
            raise

    def execute(self, query, params=None, commit=True):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        try:
            with self.connection.cursor() as cur:
                cur.execute(query, params or ())
                if commit:
                    self.connection.commit()
                if query.strip().lower().startswith("insert"):
                    return cur.lastrowid
        except Error as e:
            logging.error(" Query execution error: %s", e)
            if commit:
                self.connection.rollback()
            raise

    def fetch(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        try:
            with self.connection.cursor(dictionary=True) as cur:
                cur.execute(query, params or ())
                return cur.fetchall()
        except Error as e:
            logging.error(" Query fetch error: %s", e)
            raise

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info(" Database connection closed.")
