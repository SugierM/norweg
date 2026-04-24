from fastapi import APIRouter
from app.services.pipelines import wikitionary_to_db_pipeline


router = APIRouter()

test_data = {
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
}

@router.get('/test_words')
def import_test_words():
    wikitionary_to_db_pipeline(test_data)
    return {"message": "Test words inserted successfuly."}

