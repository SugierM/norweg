from typing import Optional, Iterable
from .base import BaseRepository
from ..models import Word
from psycopg2.extras import execute_batch


class WordRepository(BaseRepository):
    """
    Repository for Word table
    """
    def create(self, word: Word) -> Optional[int]:
        """
        
        """

        query = """
            INSERT INTO words (word, pos, language_code, lemma)
            VALUES (%(word)s, %(pos)s, %(language_code)s, %(lemma)s)
            ON CONFLICT (language_code, word, pos) DO NOTHING
            RETURNING id
        """

        result = self._execute_change(query, word.to_dict())
        return result if result else None
    

    def create_many(self, words: Iterable[Word]) -> int:
        """
        
        """
        if not words:
            return 0
        
        query = """
            INSERT INTO words (word, pos, language_code, lemma)
            VALUES %s
            ON CONFLICT (word, pos, language_code) DO NOTHING
            RETURNING language_code, word, lemma, pos, id
        """

        words_values = [(w.word, w.pos, w.language_code, w.lemma) for w in words]
        result = self._execute_values(query, words_values)
        print("OK")
        return result


    def get_by_id(self, word_id: int) -> Optional[Word]:
        """
        
        """

        query = """
            SELECT id, word, pos, language_code, lemma
            FROM words
            WHERE id = %s
        """

        row = self._execute_query_one(query, (word_id,))
        return Word.from_db_row(row) if row else None
    

    def get_by_match(self, word: str, language_code: str, pos: Optional[str] = None) -> Optional[list[Word]]:
        """
        
        """
        if pos:
            query = """
                SELECT id, word, pos, language_code, lemma
                FROM words
                WHERE word = %s AND language_code = %s AND pos = %s
            """
            params = (word, language_code, pos)

        else:

            query = """
                    SELECT id, word, pos, language_code, lemma
                    FROM words
                    WHERE word = %s AND language_code = %s
                """
            params = (word, language_code)

        rows = self._execute_query(query, params) # Words with 2 pos can be present, don't want to miss that potentially 
        return [Word.to_dict(row) for row in rows] if rows else []
    
    
    def search_by_pattern(self, pattern: str, language_code: Optional[str] = None) -> list[Word]:
        """
        
        """

        if language_code:
            query = """
                SELECT id, word, pos, language_code, lemma
                FROM words
                WHERE word ILIKE %s AND language_code = %s
                ORDER BY word
                LIMIT 100
            """
            params = (f"%{pattern}%", language_code)
        else:
            query = """
                SELECT id, word, pos, language_code, lemma
                FROM words
                WHERE word ILIKE %s
                ORDER BY word
                LIMIT 100
            """
            params = (f"%{pattern}%",)

        rows = self._execute_query(query, params)
        return [Word.from_db_row(row) for row in rows]
    

    def update(self, word_id: int, updates: dict) -> bool:
        """
        
        """

        if not updates:
            return False
        
        allowed_fields = {"word", "pos", "language_code", "lemma"}
        updates = {k: v for k, v in updates.items if k in allowed_fields}

        if not updates:
            return False
        
        change_cluase = ", ".join(f"{col} = %({col})s" for col in updates)
        updates["id"] = word_id
        
        query = f"UPDATE words SET {change_cluase} WHERE id = %(id)s"
        rowcount = self._execute_change(query, updates)

        return rowcount > 0
    

    def delete(self, word_id: int) -> bool:
        """
        
        """

        query = "DELETE FROM words WHERE id = %s"
        rowcount = self._execute_change(query, (word_id,))
        return rowcount > 0


    def get_existing_many(self, words: Iterable[tuple[str, str, str]]) -> list[dict]:
        """
        word, pos, language_code        
        """
        query = """
            SELECT w.id, w.word, w.pos, w.language_code, w.lemma 
            FROM words w
            JOIN (
                VALUES %s
            ) AS v(word, pos, language_code)
            ON w.word = v.word AND w.pos = v.pos AND w.language_code = v.language_code
        """

        return self._execute_values(query, words, template="(%s, %s, %s)")


    # Not implemented yet, same as for WORD REPO
    def find_lemma_words(self, lemma: str, direction: str) -> list[Word]:
        """
        
        """
        if direction:
            query = """
                SELECT
                    t.id AS translation_id,
                    sw.word AS source_word,
                    sw.language_code AS source_language,
                    tw.word AS target_word,
                    tw.language_code AS target_language,
                    sw.lemma AS lemma
                FROM translations t
                JOIN words sw ON t.source_word_id = sw.id
                JOIN words tw ON t.target_word_id = tw.id
                WHERE sw.lemma = tw.lemma
                AND sw.lemma = %s
                AND direction = %s
            """

            params = (lemma, direction)
        else:
            query = """
                SELECT
                    t.id AS translation_id,
                    sw.word AS source_word,
                    sw.language_code AS source_language,
                    tw.word AS target_word,
                    tw.language_code AS target_language,
                    sw.lemma AS lemma
                FROM translations t
                JOIN words sw ON t.source_word_id = sw.id
                JOIN words tw ON t.target_word_id = tw.id
                WHERE sw.lemma = tw.lemma
                AND sw.lemma = %s
            """
            params(lemma,)

        rows = self._execute_query(query, params)
        return rows
    
