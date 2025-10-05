from dataclasses import dataclass
from typing import Optional 

@dataclass
class Word:
    """
    
    """

    word: str
    language_code: str
    lemma: str
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
            id=row["id"],
            word=row["word"],
            language_code=row["language_code"],
            lemma=row["lemma"],
            pos=row.get("pos"),
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
        }


    @classmethod
    def from_db_row(cls, row: dict) -> "Translation":
        """
        
        """
        
        return cls(
            id=row["id"],
            source_word_id=row["source_word_id"],
            target_word_id=row["target_word_id"],
            direction=row["direction"],
        )