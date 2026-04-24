# TAKE JSON FROM PIPELINE
# {'pytt': {'translations': [{'pos': 'noun','en_translation': [...], 'pl_translation': [...]}, ...], 'lemma': 'pyte'}, ...}
#               there can be not norwegian word presnet in db!

# CHECK WHAT WORDS ARE PRESENT IN DB - pos, language_code and word_itself
# CREATE WORD AND TRANSLATION
# SAVE WORDS AND TRANSLATIONS

from app.normalizers.word_mappers import json_to_list as json_to_list_words
from app.normalizers.translation_mappers import json_to_list as json_to_list_trans
from app.database.repositories import word_repo, trnas_repo

from app.database.models import Word, Translation


# Not what i wanted, need to work this out
def wikitionary_to_db_words(response: dict) -> tuple[list[Word], list[Word]]:
    """
    
    """
    # Check existing
    word_list, norw_lemmas = json_to_list_words(response) # -> [(word, pos, lang_code), ...], {norwegian_word: its_lemma}
    word_set = set(word_list)
    existing_ =  word_repo.get_existing_many(word_set) 
    existing_set = {(row["word"], row["pos"], row["language_code"]) for row in existing_} # -> {(word, pos, lang_code), ...}

    # Find missing ones
    missing = word_set - existing_set
    if not missing:
        print("Everything already in database.")
        existing_words = [Word.from_db_row(row) for row in existing_] # With id 
        return (existing_words, [])
    # Save to db
    new_ = word_repo.create_many([Word.from_db_row({
                "word": row[0],
                "pos": row[1],
                "language_code": row[2],
                "lemma": norw_lemmas.get(row[0])
            }) 
            for row in missing
        ])
    
    # Create Word instances
    existing_words = [Word.from_db_row(row) for row in existing_] # With id 
    new_words = [Word.from_db_row(row) for row in new_] # With id
    return (existing_words, new_words)


# Translations
def wikitionary_to_db_transltions(json_response: dict, existing_words: list[Word], new_words: list[Word]) -> list[Translation]:
    """
    
    """
    existing_words.extend(new_words)
    search_dict = dict()
    for word in existing_words:
        search_dict[(word.word, word.pos, word.language_code)] = word.id
    
    translations_list = json_to_list_trans(json_response, search_dict)
    return [Translation.from_db_row(row) for row in trnas_repo.create_many(translations_list)] # Return only new ones as for now

