from app.utils.variables import *

def json_to_list(response: dict) -> list:
    """
    
    """
    for word, data in response:
        # word = 'word'
        # data = 'translations': [{'pos': '...','en_translation': ['...', ...],
        #                                    'pl_translation': ['...', ...]},
        #                     {'pos': '...','en_translation': ['...', ...],
        #                                    'pl_translation': ['...', ...]}
        # ...], lemma = '...'
        pass