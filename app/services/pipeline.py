from clients.class_http import WikitionaryClient
from utils.text_manipulation import *
from utils.utils import *
from time import time

# Not implemented fully
def preparation_pipeline(img_path: str, parser: WikitionaryClient, chunk_size: int = 3) -> dict:
    """
    
    """
        # For quick tests
    # words_info = {'pytt': [{
    #             'pos': 'noun',
    #             'en_translation': ['a pond', 'pool (of water)', 'puddle']
    #                 }],
    #         'vennen': [{
    #             'pos': 'noun',
    #             'en_translation': ['definite singular of venn']
    #         }],
    #         'drikke': [{
    #             'pos': 'noun',
    #             'en_translation': ['drink']},
    #                 {
    #             'pos': 'verb',
    #             'en_translation': ['to drink']
    #                 }]}


    text = extract_text(img_path) # -> Some raw text
    word_list = create_word_list(text) # -> ["hei", "verden", "hun", "istotny", "hus3"] --- List of possible words (polish chars and numbers)
    word_list = seek_norwegian(word_list) # -> ["hei", "verden", "hun"] --- Filtered list consisting only of Norwegian words
    words_info = parser.process_words(word_list) # -> {'drikke': [{'pos': 'noun', 'en_translation': ['drink']} ...,}


    # Split it into chunks, as with longer context LLMs start to bug out. 
    # In a local environment, it mainly becomes a time issue.
    keys = list(words_info.keys())
    len_words = len(keys)
    proper_dict = dict() # Should have proper structure for database

    skipped_words = []

    for i in range(0, len_words, chunk_size):
        temp = keys[i: min(i+chunk_size, len_words)]
        prop: dict = {key: words_info[key] for key in temp} 

        try:
            t = analyze_text(prop) # -> {'drikke': [{'pos': 'noun', 'en_translation': ['drink'], 'pl_translation': ['napój']} ...,} | str: list
            lemmas = get_lemmas(temp) # -> {word: its_lemma, ...}
            
            for key in lemmas.keys():
                proper_dict[key] = dict()
                proper_dict[key]["translations"] = t[key]
                proper_dict[key]["lemma"] = lemmas[key]

        except Exception as e:
            print(type(e))
            print(e)


    return proper_dict # -> {'pytt': {'translations': [{'pos': 'noun','en_translation': [...], 'pl_translation': [...]}, ...], 'lemma': 'pyte'}, ...}
        
if __name__ == "__main__":
    # print(preparation_pipeline("does not matter", WikitionaryClient()))
    print(preparation_pipeline("img/img_170920251644.png", WikitionaryClient())) 

