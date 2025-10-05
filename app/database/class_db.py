from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import sql, extras
from typing import Optional

load_dotenv()

class NorwegDB:
    def __init__(self):
        """
        
        """
        self.conn_params = {
            "dbname": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST", "localhost"),
        }

        if not self.conn_params["password"]:
            raise ValueError(
                "POSTGRES_PASSWORD must be set in environment or .env file"
            )
        
        self.conn: Optional[psycopg2.extensions.connection] = None
        self.cursor: Optional[extras.RealDictCursor] = None
        self.connect()
        self.ensure_schema()


    def connect(self):
        """
        
        """
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cursor = self.conn.cursor(
                cursor_factory = extras.RealDictCursor
            )
            print(f"Connection to DB: {self.conn_params["dbname"]} established.")

        except psycopg2.Error as e:
            print(f"Connection failed: {e}.")
            raise # Investigate


    def ensure_schema(self):
        """
        
        """
        print("Database schema check.")

        self.cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('words', 'translations')
        """)

        # Check for tables
        existing_tables = [row["table_name"] for row in self.cursor.fetchall()]

        if "words" in existing_tables and "translations" in existing_tables:
            print("Schema tests were successful.")

        else:
            print("Missing tables. Creating proper schema.")
            self._create_tables()


    def _create_tables(self):
        """
        
        """
        try:
            ################################################################ Words
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS words (
                    id SERIAL PRIMARY KEY,
                    language_code VARCHAR(5) NOT NULL,
                    word VARCHAR(120) NOT NULL,
                    lemma VARCHAR(120) NOT NULL,
                    pos VARCHAR (50),
                    UNIQUE(language_code, word, pos)
                )
            """)

            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_words_language_word
                ON words(language_code, word)
            """)

            ############################################################ Translations
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS translations (
                    id SERIAL PRIMARY KEY,
                    source_word_id INTEGER NOT NULL,
                    target_word_id INTEGER NOT NULL,
                    direction VARCHAR(12) NOT NULL,
                    FOREIGN KEY (source_word_id) REFERENCES words(id) 
                        ON DELETE CASCADE,
                    FOREIGN KEY (target_word_id) REFERENCES words(id) 
                        ON DELETE CASCADE,
                    UNIQUE(source_word_id, target_word_id, direction)
                )
            """)

            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_translations_source 
                ON translations(source_word_id)
            """)
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_translations_target 
                ON translations(target_word_id)
            """)

            self.conn.commit()

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error creating tables: {e}.")
            

    def add_word(self, word_data) -> Optional[int]:
        """
        
        """
        try: 
            self.cursor.execute("""
                INSERT INTO words (language_code, word, lemma, pos)
                VALUES (%(language_code)s, %(word)s, %(lemma)s, %(pos)s)
                ON CONFLICT (language_code, word, pos) DO NOTHING
                RETURNING id
            """, word_data)

            result = self.cursor.fetchone()["id"]
            self.conn.commit()
            if result:
                return result
            else:
                print("Word already in database.")
                return None
            
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error occured during inserting the word: {e}")
            return None
        
    
    def get_word_by_id(self, id: int) -> Optional[dict]:
        """
        
        """
        try:
            self.cursor.execute("""
                    SELECT id, word, language_code, lemma, pos
                    FROM words
                    WHERE id = %s
                """, (id,))
            
            result = self.cursor.fetchone()
            return result

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error occured during extracting the word: {e}")
            return None


    def get_word_by_name(self, name: str) -> Optional[dict]:
        """
        
        """
        try:
            self.cursor.execute("""
                    SELECT id, word, language_code, lemma, pos
                    FROM words
                    WHERE id = %s
                """, (name,))
            
            return self.cursor.fetchone()

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error occured during extracting the word: {e}")
            return None


    def get_word_by_part(self, part: str) -> Optional[dict]:
        """
        
        """
        try:
            self.cursor.execute("""
                    SELECT id, word, language_code, lemma, pos
                    FROM words
                    WHERE word ILIKE %(part)s
                """, {"part": f"%{part}%"})
            
            return self.cursor.fetchall()

        except psycopg2.Error as e:
            print(f"Error occured during word search: {e}")
            return None


    # Add something to remember about cascade effect
    def delete_word(self, id: int) -> Optional[dict]:
        """
        
        """
        try:
            self.cursor.execute("DELETE FROM words WHERE id = %s", (id,))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                print("Word deleted successfuly.")
                return True
            
            else:
                print(f"Word with id: {id} not found.")
                return False

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error occured during deleting the word: {e}")
            return False
        

    # Make it more robust in the future
    def update_word(self, id: int, updates: dict) -> bool: 
        """
        
        """
        if not updates:
            print("There are no information to update.")
            return False
        
        update_fields = ", ".join(f"{col} = %({col})s" for col in updates.keys())
        updates["id"] = id
        query = f"UPDATE words SET {update_fields} WHERE id = %(id)s"


        try:
            self.cursor.execute(query, updates)
            self.conn.commit()
            return True

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error occured during updating the word: {e}.")
            return False

