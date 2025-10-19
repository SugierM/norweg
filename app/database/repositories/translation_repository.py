from typing import Optional, Iterable
from .base import BaseRepository
from ..models import Translation, Word

    # source_word_id: int
    # target_word_id: int
    # direction: str

class WordRepository(BaseRepository):
    """
    Repository for Word table
    """

    def create(self, translation: Translation) -> Optional[int]:
        """
        
        """

        query = """
            INSERT INTO translations (source_word_id, target_word_id, direction)
            VALUES (%(source_word_id)s, %(target_word_id)s, %(direction)s)
            ON CONFLICT (source_word_id, target_word_id, direction) DO NOTHING
            RETURNING id
        """

        result = self._execute_change(query, translation.to_dict())
        return result if result else None
    

    def create_many(self, translations: list[Translation]) -> int: # For now only rowcount.
        """
        
        """
        if not translations:
            return 0
        
        query = """
            INSERT INTO translations (source_word_id, target_word_id, direction)
            VALUES %s
            ON CONFLICT (source_word_id, target_word_id, direction) DO NOTHING
            RETURNING id
        """

        translations_values = [(t.source_word_id, t.target_word_id, t.direction) for t in translations]
        result = self._execute_values(query, translations_values)
        return result


    def get_by_id(self, translation_id: int) -> Optional[Translation]:
        """
        
        """

        query = """
            SELECT id, source_word_id, target_word_id, direction
            FROM translations
            WHERE id = %s
        """

        row = self._execute_query_one(query, (translation_id,))
        return Translation.from_db_row(row) if row else None
    

    def get_translation_for_word(self, word_id: int, direction: Optional[str] = None) -> list[Word]:
        """
        
        """
        if direction:
            query = """
                SELECT w.id, w.word, w.language_code, w.lemma, w.pos
                FROM translations t
                JOIN words w ON w.id = t.target_word_id
                WHERE t.source_word_id = %s AND t.direction = %s
            """

            params = (word_id, direction)

        else:
            query = """
                SELECT w.id, w.word, w.language_code, w.lemma, w.pos
                FROM translations t
                JOIN words w ON w.id = t.target_word_id
                WHERE t.source_word_id = %s
            """
            params = (word_id,)

        rows = self._execute_query(query, params)
        return [Word.from_db_row(row) for row in rows]
    

    def update(self, translation_id: int, updates: dict) -> bool:
        """
        
        """

        if not updates:
            return False
        
        allowed_fields = {"source_word_id", "target_word_id", "direction"}
        updates = {k: v for k, v in updates.items if k in allowed_fields}

        if not updates:
            return False
        
        change_cluase = ", ".join(f"{col} = %({col})s" for col in updates)
        updates["id"] = translation_id
        
        query = f"UPDATE translations SET {change_cluase} WHERE id = %(id)s"
        rowcount = self._execute_change(query, updates)

        return rowcount > 0
    

    def delete(self, translation_id: int) -> bool:
        """
        
        """

        query = "DELETE FROM translations WHERE id = %s"
        rowcount = self._execute_change(query, (translation_id,))
        return rowcount > 0


    def delete_all_translations_involving(self, word_id: int) -> int:
        """
        
        """

        query = """
            DELETE FROM translations 
            WHERE source_word_id = %s OR target_word_id = %s
        """
        return self._execute_change(query, (word_id, word_id))


    def get_existing_many(self, translations: Iterable[tuple[int, int, str]]) -> list[dict]:
        """
        
        """
        query = """
            SELECT t.source_word_id, t.target_word_id, t.direction, t.id
            FROM translations t
            JOIN (
                VALUES %s
            ) AS v(source_word_id, target_word_id, direction)
            ON t.source_word_id = v.source_word_id
            AND t.target_word_id = v.target_word_id
            AND t.direction = v.direction
        """
        return self._execute_values(query, translations, template="(%s, %s, %s)")


    # Not implemented yet, same as TRNASLATION REPO
    def find_lemma_translations(self, lemma: str, direction: str) -> list[Translation]:
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