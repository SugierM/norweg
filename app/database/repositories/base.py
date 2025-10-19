from typing import Optional
from psycopg2.extras import execute_batch, execute_values
from ..connection import NorwegDBConnection

class BaseRepository:
    """
    Base class for all repositories. (High level of what they do.)
    """

    def __init__(self, db: NorwegDBConnection):
        self.db = db
        self.db.c

    def _execute_query(self, query: str, params: Optional[tuple | dict] = None) -> list[dict]:
        """
        Execute SELECT and return all results.
        """

        with self.db.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
        

    def _execute_query_one(self, query: str, params: Optional[tuple | dict] = None) -> Optional[dict]:
        """
        Execute SELECT and return first result.
        """

        with self.db.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()
        

    def _execute_change(self, query: str, params: Optional[tuple | dict] = None) -> int:
        """
        Execute INSERT, UPDATE, DELETE and return number of affected rows.
        """

        with self.db.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
        

    def _execute_change_returning(self, query: str, params: Optional[tuple | dict] = None) -> list:
        """
        Execute INSERT, UPDATE, DELETE and return results of changes.
        """

        with self.db.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
        

    def _execute_batch(self, query: str, params_list: list[dict | tuple], page_size: int = 100) -> int:
        """

        """

        if not params_list:
            return 0

        with self.db.get_cursor() as cursor:
            execute_batch(cursor, query, params_list, page_size=page_size)
            return cursor.rowcount
        
################
    def _execute_values(self, query: str,
                        params_list: list[dict | tuple],
                        template: Optional[str] = None,
                        page_size: int = 100,
                        fetch=True
                        ) -> list[dict]:
        """
        Write something just to make it orange between all text text, I see method now. MAYBE
        """

        if not params_list:
            return []
        
        with self.db.get_cursor() as cursor:
            execute_values(
                cursor,
                query,
                params_list,
                template=template,
                page_size=page_size,
                fetch=fetch
            )

            try:
                return cursor.fetchall()
            except: # If sql query doesn't have RETURNING
                return [] # May have a problem with debugging


################