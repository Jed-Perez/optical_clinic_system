import mysql.connector
from mysql.connector import Error
from database.db_config import DB_CONFIG
from utils.logger import setup_logging

logger = setup_logging(__name__)


class Database:
    def __init__(self, raise_on_error=False):
        self.last_error = None
        self.raise_on_error = raise_on_error
        # Try to connect; if we get a 1045 access denied and host is localhost/127.0.0.1
        # attempt the alternate host once (some MySQL installs treat localhost vs 127.0.0.1 differently).
        tried_alternate = False
        cfg = dict(DB_CONFIG)
        tried_hosts = []
        while True:
            host = cfg.get('host')
            tried_hosts.append(host)
            try:
                self.connection = mysql.connector.connect(**cfg)
                if self.connection.is_connected():
                    logger.info(f"Connected to database (host={host})")
                break
            except Error as e:
                self.last_error = e
                # if access denied and we haven't tried swapping localhost/127.0.0.1, try the other
                err_no = getattr(e, 'errno', None)
                logger.error(f'DB connection error (host={host}): {str(e)}')
                if err_no == 1045 and not tried_alternate:
                    tried_alternate = True
                    # swap host between 'localhost' and '127.0.0.1'
                    alt = None
                    if host == '127.0.0.1':
                        alt = 'localhost'
                    elif host == 'localhost':
                        alt = '127.0.0.1'
                    if alt:
                        logger.info(f"Trying alternate host '{alt}' due to auth failure...")
                        cfg['host'] = alt
                        continue
                # no alternate to try or alternate already tried -> give up
                self.connection = None
                if self.raise_on_error:
                    error_msg = f"Failed to connect to database. Last error: {e}"
                    if tried_hosts:
                        error_msg += f" (tried hosts: {', '.join(tried_hosts)})"
                    logger.critical(error_msg)
                    raise RuntimeError(error_msg)
                break

    def is_connected(self):
        return bool(self.connection and getattr(self.connection, 'is_connected', lambda: False)())

    def execute(self, query, params=None):
        if not self.connection:
            err = f'No DB connection. Last error: {self.last_error}'
            raise RuntimeError(err)
        cur = self.connection.cursor()
        try:
            cur.execute(query, params or ())
            self.connection.commit()
            return cur.lastrowid
        finally:
            cur.close()

    def fetch(self, query, params=None):
        if not self.connection:
            err = f'No DB connection. Last error: {self.last_error}'
            raise RuntimeError(err)
        cur = self.connection.cursor(dictionary=True)
        try:
            cur.execute(query, params or ())
            return cur.fetchall()
        finally:
            cur.close()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
