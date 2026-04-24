from app.utils.variables import Languages

def json_to_list(json_response: dict) -> list[tuple[str, str, str]]:
    """
    word, pos, language_code 
    """
    word_list = []
    lemmas = dict()
    for word, data in json_response.items():
        # word = 'word'
        # data = 'translations': [{'pos': '...','en_translation': ['...', ...],
        #                                    'pl_translation': ['...', ...]},
        #                     {'pos': '...','en_translation': ['...', ...],
        #                                    'pl_translation': ['...', ...]}
        # ...], lemma = '...'
        transaltions: list = data["translations"]
        for t in transaltions:
            pos = t["pos"]
            eng_translations = t["en_translation"]
            pl_translations = t["pl_translation"]
            word_list.extend([(word, pos, Languages.NORW_CODE.value)] + 
                             [(e, pos, Languages.ENG_CODE.value) for e in eng_translations] + 
                             [(p, pos, Languages.PL_CODE.value) for p in pl_translations])
        lemmas[word] = data["lemma"]
            
    return word_list, lemmas
      




if __name__ == "__main__":
    print(json_to_list({
  'pytt': {
    'translations': [
      {
        'pos': 'noun',
        'en_translation': [
          'a pond',
          'pool (of water)',
          'puddle'
        ],
        'pl_translation': [
          'staw',
          'basen',
          'kałuża'
        ]
      }
    ],
    'lemma': 'pyte'
  },
  'vennen': {
    'translations': [
      {
        'pos': 'noun',
        'en_translation': [
          'definite singular of venn'
        ],
        'pl_translation': [
          "liczba pojedyncza określona od 'venn' (przyjaciel)"
        ]
      }
    ],
    'lemma': 'venn'
  },
  'drikke': {
    'translations': [
      {
        'pos': 'noun',
        'en_translation': [
          'drink'
        ],
        'pl_translation': [
          'napój'
        ]
      },
      {     
        'pos': 'verb',
        'en_translation': [
          'to drink'
        ],
        'pl_translation': [
          'pić'
        ]
      }
    ],
    'lemma': 'drikke'
  }
}))