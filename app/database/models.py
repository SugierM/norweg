from dataclasses import dataclass
from typing import Optional 

@dataclass
class Word:
    """
    
    """

    word: str
    language_code: str
    lemma: Optional[str] = None
    pos: str
    id: Optional[int] = None

    def to_dict(self) -> dict:
        """
        
        """
        return {
            "word": self.word,
            "language_code": self.language_code,
            "lemma": self.lemma,
            "pos": self.pos,
        }
    

    @classmethod
    def from_db_row(cls, row: dict) -> "Word":
        """
        
        """
        return cls(
            word=row["word"],
            language_code=row["language_code"],
            pos=row["pos"],
            lemma=row.get("lemma"),
            id=row.get("id"),
        )
    

@dataclass
class Translation:
    """
    
    """

    source_word_id: int
    target_word_id: int
    direction: str
    id: Optional[int] = None

    def to_dict(self) -> dict:
        """
        
        """
        return {
            "source_word_id": self.source_word_id,
            "target_word_id": self.target_word_id,
            "direction": self.direction,
            "id": self.id
        }


    @classmethod
    def from_db_row(cls, row: dict) -> "Translation":
        """
        
        """
        
        return cls(
            id=row.get("id"),
            source_word_id=row["source_word_id"],
            target_word_id=row["target_word_id"],
            direction=row["direction"],
        )