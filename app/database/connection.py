from contextlib import contextmanager
from typing import Optional, Generator
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv
import os

load_dotenv()


class NorwegDBConnection:
    """
    
    """

    def __init__(self):
        self.conn_params = {
            "dbname": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": os.getenv("POSTGRES_PORT", "5432"),
        }

        if not self.conn_params["password"]:
            raise ValueError("POSTGRES_PASSWORD must be set in environment")
        
        self._conn: Optional[psycopg2.extensions.connection] = None


    def connect(self) -> psycopg2.extensions.connection:
        """
        
        """

        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(**self.conn_params)

        return self._conn
            
    
    def close(self):
        """
        
        """

        if self._conn and not self._conn.closed:
            self._conn.close()
            self._conn = None

    
    @contextmanager
    def get_cursor(self) -> Generator[extras.RealDictCursor, None, None]:
        """
        
        """

        conn = self.connect()
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        
        try:
            yield cursor
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise

        finally:
            cursor.close()

    @property
    def conn(self) -> psycopg2.extensions.connection: # conn = db.conn as property not a function
        """
        
        """
        return self.connect()
        

db = NorwegDBConnection()