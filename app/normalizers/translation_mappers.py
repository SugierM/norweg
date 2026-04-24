from app.utils.variables import *
from app.database.models import Word, Translation

def json_to_list(response: dict, words: dict[tuple[str, str, str], int]) -> list[Translation]:
    """
    
    """
    translations = []
    for word, data in response.items():
        # word = 'word'
        # data = 'translations': [{'pos': '...', 'en_translation': ['...', ...],
        #                                    'pl_translation': ['...', ...]},
        #                     {'pos': '...', 'en_translation': ['...', ...],
        #                                    'pl_translation': ['...', ...]}
        # ...], lemma = '...'
        temp: list[dict] = data["translations"]
        for t in temp: # t: dict
            # For NORW->ENG
            pos = t["pos"]
            word_id = words[(word, pos, Languages.NORW_CODE.value)]
            translations.extend([Translation.from_db_row({
                "source_word_id": word_id,
                "target_word_id": words[(trans, pos, Languages.ENG_CODE.value)],
                "direction": Directions.DIRECTION_NORW_ENG.value
            }) for trans in t["en_translation"]])
            
            # FOR ENG->PL With not assured assumption for now
            for i in range(len(t["en_translation"])):
                translations.extend([Translation.from_db_row({
                "source_word_id": words[(t["en_translation"][i], pos, Languages.ENG_CODE.value)],
                "target_word_id": words[(t["pl_translation"][i], pos, Languages.PL_CODE.value)],
                "direction": Directions.DIRECTION_ENG_PL.value 
                })])

    return translations

            