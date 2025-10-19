# TAKE JSON FROM PIPELINE
# {'pytt': {'translations': [{'pos': 'noun','en_translation': [...], 'pl_translation': [...]}, ...], 'lemma': 'pyte'}, ...}
#               there can be not norwegian word presnet in db!

# CHECK WHAT WORDS ARE PRESENT IN DB - pos, language_code and word_itself
# CREATE WORD AND TRANSLATION
# SAVE WORDS AND TRANSLATIONS

from app.normalizers.word_mappers import json_to_list
from app.database.repositories.word_repository import WordRepository
from app.database.models import Word


# Not what i wanted, need to work this out
def wikitionary_to_db_words(response: dict) -> tuple[list[dict], list[dict]]:
    """
    
    """
    # Check existing
    word_list, norw_lemmas = json_to_list(response) # -> [(word, pos, lang_code), ...], {norwegian_word: its_lemma}
    word_set = set(word_list)
    existing_words =  WordRepository.get_existing_many(word_set) 
    existing_set = {(row["word"], row["pos"], row["language_code"]) for row in existing_words} # -> {(word, pos, lang_code), ...}

    # Find missing ones
    missing = word_set - existing_set
    if not missing:
        print("Everything already in database.")
        return {"successes": 0, "fails": [], "present": len(word_set)}
    
    # Save to databse
    new_words = WordRepository.create_many([
        Word.from_db_row({
                "word": row[0],
                "pos": row[1],
                "language_code": row[2],
                "lemma": norw_lemmas.get(row[0])
            }) 
            for row in missing
        ])
    
    return (existing_words, new_words)


# Translations
def wikitionary_to_db_transltions(existing_words: list, new_words: list) -> dict:
    """
    
    """
    pass

