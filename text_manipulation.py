# from doctr.io import DocumentFile
# from doctr.models import ocr_predictor
from utils import *
import os
from typing import List
import pytesseract
from PIL import Image
from dotenv import load_dotenv
from spylls.hunspell import Dictionary

load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.environ.get("TESSERACT_PATH")
# Dictionary
DIC_PATH = os.path.join("norw_dictionaries", os.environ.get("DICTIONARY"))
NORW_DIC = Dictionary.from_files(DIC_PATH)

# There is high chance that model will be changed, its just PoC even for scope of this project, maybe XD
def analyze_text(text: List[str]) -> dict:
    """
    Analyze words with LLM to translate them and give meaning begind them.

    Args:
        text - list of words that will be translated
    
    Returns:
        A dictionary containing  two keys with given values:
            - To be determined
    """
# ___________________________________________________________________________________________________________


    prompt = f"""
Use concise internal reasoning (thinking: low).
Du er en assistent som kun skal returnere gyldig JSON. Ikke legg til kommentarer eller ekstra tekst; returner kun JSON.

Oppgave:

1. Du vil motta en liste med norske ord (substantiv, verb osv.).
2. For hvert ord: returner opptil tre av de vanligste oversettelsene til polsk.
3. For hver oversettelse: legg til en kort forklaring på polsk (enkel, ordbok-stil).
4. Hvis et ord har færre enn tre vanlige oversettelser, returner bare de som er vanlige.
5. Behold nøyaktig JSON-strukturen vist nedenfor (med riktige nøkkelnavn og nesting). Bruk det norske ordet som toppnivånøkkel.
6. Ikke finn på ekstra felt. Ikke ta med forklaringer, notater eller eksempler utenfor JSON.

Output JSON example:

{{
  "bok": [
    {{"oversettelse": "książka", "betydning": "zbiór zapisanych stron"}},
    {{"oversettelse": "tom", "betydning": "jeden egzemplarz książki"}},
    {{"oversettelse": "album", "betydning": "zbiór ilustracji lub zdjęć"}}
  ]
}}

Input words (Norwegian):

{text}

"""

    data = handle_json_response(prompt)
    ########
    return data 


def extract_text(image_path: str) -> str:
    """
    Extracts text from an image by first straightening it and then applying OCR.

    This function takes a relative path to an image file,
    attempts to straighten the image to improve OCR accuracy, and then
    uses a pre-trained OCR model to extract text from the processed image.

    Args:
        image_path: The relative path to the input image file.
                    Example: "data/my_document.png"

    Returns:
        The extracted text as a single string from the image.
    """

    # Straighten image for better ocr --- Not with pytesseract i think -> for further investigation for now
    # folder, image = os.path.split(image_path) # Format needed for straighten_image function
    # straighten_image(folder, image)
    # straighten_image_path = straighten_img_path(folder, image)

    # Extract text
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="nor+pol")
        print("_" * 20, "RAW TEXT", "_" * 20)
        print(text)
        print("_" * 25, "_" * 25)
        return text
    except Exception as e:
        print("Error during reading text from image.")
        print(type(e))
        print(f"Error: {e}")
        return None

    

    #__________________________OLD VERSION_____________________________
    # Extract text
    # straighten_image_path = straighten_img_path(folder, image) # Straighten image has new name
    # ocr_model = ocr_predictor(det_arch="db_resnet50", reco_arch="crnn_mobilenet_v3_large", pretrained=True)
    # doc = DocumentFile.from_images(straighten_image_path)
    # return ocr_model(doc).render()

# Different aproach with preprocessing words. Will be changed
def clean_accents(data: dict) -> dict:
    """
    Cleans incorrect accents in Norwegian words within a dict.

    Args:
        words: List of strings.
               Example: ['pâ', 'âr', 'Nâ']

    Returns:
        A new list with corrected accents in the words.
        Example: ['på', 'år', 'Nå']
    """
    # For simpler task
    temp = {"words": data["words"], "sentences": data["sentences"]}
    prompt = f"""
Du er en assistent som kun snakker i JSON. Ikke bruk vanlig språk og ikke legg til kommentarer, du bruker kun JSON. Du har fått følgende oppgave:
1. Denne JSON-en inneholder ord og setninger på norsk, men med feil staving - korriger dem.
2. Behold alle ordene og setningene, men sørg for at de er riktig stavet.
3. Ikke endre strukturen på JSON-en du fikk.

JSON:
{temp}
"""

    # Utilize LLM to correct everything
    new_data = handle_json_response(prompt)
    try:
        assert data["words_len"] == len(new_data["words"])

    # As for now I just want to know it
    except AssertionError as e:
        print("Responses doesn't match")
    
    return new_data


def create_word_list(text: str) -> List[str]:
    """
    Splits a given text into a set of cleaned, unique words.
    Words containing special characters, Polish diacritic letters, or digits are omitted.
    Args:
        text: The input string to be processed.
              Example: "Hei verden! Cześć 123 hun..."

    Returns:
        A set of unique, cleaned, lowercase words extracted from
        the input text.
                Example: ["hei", "verden", "hun"]
    """
    words = set()
    skipped = set("ąćęłńóśźż0123456789")
    for word in text.split():
        # Skip if it contains undesired characters
        if any(char in skipped for char in word):
            continue

        # Keep only chars
        clean = "".join(char for char in word.lower() if char.isalpha())

        # Skip empty strings
        if clean:
            words.add(clean)
    
    print("_" * 20, "AFTER SPLIT", "_" * 20)
    print(words)
    print("_" * 25, "_" * 25)
    return words


def seek_norwegian(words: List[str]) -> List[str]:
    """
    Filters a list of words, keeping only those found in a Norwegian dictionary.

    This function checks each input word against a pre-loaded Norwegian
    dictionary resource (based on the "nb" dictionary from the "wooorm/dictionaries"
    project). Words that are recognized as valid Norwegian terms are collected and
    returned, while all others are excluded.

    Args:
        words: A list of candidate words to evaluate.
               Example: ["hei", "world", "takk", "apple"]

    Returns:
        A list containing only the words that match entries
        in the Norwegian dictionary.
    """
    norw_words = []
    for word in words:
        if NORW_DIC.lookup(word):
            norw_words.append(word)

    return norw_words


def create_dict(words: List[str]) -> dict:
    """
    
    """
    to_ret = dict()
    len_words = len(words)

    # Split words in to chunks of 3, as with longer promopts
    # LLM start to reapet words. With local environment it's time issue.
    for i in range(0, len_words, 3):
        prop: dict = analyze_text(words[i: min(i+3, len_words)])
        words_skipped = []

        # As maybe there will be better way to handle it that just get rid off it
        # Introduce block that will handle it.
        try:
            validate_dict(prop)
            
        except StructureError as e:
            print("Error occured for:\n", prop)
            print(f"Error: {e}")
            words_skipped += words[i: min(i+3, len_words)]
            continue # Maybe others are good

        # Maybe not good idead for production env.
        except Exception as e:
            print("Error occured for:\n", prop)
            print("Need to evaluate if validation is created properly.")
            words_skipped += words[i: min(i+3, len_words)]
            continue # Maybe others are good

        to_ret.update(prop)
    if words_skipped:
        print(f"Skipped words: {words_skipped}")

    return to_ret

        

if __name__ == "__main__":
    test = "Zdania proste 1 Helsetninger 1 | FRP sino86, która jest istotna do tego, by zrozumieć Części zdania w zdaniu prostym mają ustaloną kolejność, która j Przekaz, wane treŚci. å . | å + sh 1 F ai 1 i n i i Zdanie w języku norweskim musi zawierać podmiot i orzeczenie. Znajdują py 8 oi Orzeczen; A jest zawsze na drugim miejscu, podmiot na pierwszym lub, jeśli pierwsze miejsce jest zajęte, na trzecim. Przykład Hun danser i kveld. (Ona tańczy dziś wieczorem.) I kveld danser hun. (Ona tańczy dziś wieczorem.) B Jeśli w zdaniu występuje okolicznik zdaniowy (np. IKKE, OFTE, SJELDEN, ALLTID, ALDRI, JO), t0 znajduje się tuż za orzeczeniem. Jeśli za orzeczeniem stoi podmiot, to związek podmiot-orzeczenie nie może uler rozbiciu i okolicznik zdaniowy przechodzi za podmiot. Przykład Hun danser ikke i kveld. (Ona nie tańczy dziś wieczorem.) I kveld danser hun ikke. (Ona nie tańczy dziś wieczorem.) Ę Jeśli orzeczenie w zdaniu jest złożone (np. perfektum, futurum), to okolicznik zdaniowy znajduje się za łącz- nikiem (pierwsza część orzeczenia). Jeśli pierwsze miejsce w zdaniu jest zajęte nie przez podmiot, to nie ulega rozbiciu związek podmiot-łącznik i okolicznik zdaniowy przesuwa się za podmiot. Przykład Hun skal danse i kveld. (Ona będzie tańczyć dziś wieczorem.) Hun skal ikke danse i kveld. (Ona nie będzie tańczyć dziś wieczorem.) I kveld skal hun danse. (Ona będzie tańczyć dziś wieczorem.) I kveld skal hun ikke danse. (Ona nie będzie tańczyć dziś wieczorem.) D Na końcu zdania jest miejsce na dopełnienie, następnie zaś na okolicznik (najpierw miejsca, potem czasu)."
    norw_test = "Hun"
    analyze_test = ["haug", "hus", "venn", "jeg"]
    print(create_dict(analyze_test))