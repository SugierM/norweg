from app.database.repositories import word_repo, trnas_repo
from app.utils.variables import Languages, Directions
from app.database.models import *
from typing import Optional

def get_polish_from_norwegian(word: str) -> dict:
    """
    {word:[
            pos:{
                    eng_word: pol_word, 
                    ...
            }, 
            ...
    
    ]}
    """
    norw_words: Optional[list[Word]] = [Word.from_db_row(row) for row in word_repo.get_by_match(word=word, language_code=Languages.NORW_CODE.value)]
    # This will return list of norwegian words that will only differ by a pos.

    # [{"word":"pytt","language_code":"no","pos":"noun","lemma":"pyte","id":null}]
    if not norw_words:
        return dict({"message": f"There are no norwegian words matching - {word}"})
    
    # As there can be many pos (verb, noun...)
    eng_words = dict()
    for w in norw_words:
        pairs = dict()
        english_translations: list[Word] = trnas_repo.get_translation_for_word_id(w.id)
        for et in english_translations:
            pairs[et.word] = [transla.word for transla in trnas_repo.get_translation_for_word_id(et.id)]
        eng_words[w.pos] = pairs
    
    return {norw_words[0].word: eng_words} # Can be by and index as all words will be the same

