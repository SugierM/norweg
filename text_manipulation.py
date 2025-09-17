import json
import ollama
import re
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from utils import *
import os
from typing import List, Dict

# There is no validation for the structure
# There is high chance that model will be changed, its just PoC even for scope of this project, maybe XD
def analyze_text(text) -> dict:
    """
    Analyze text with LLM to identify norwegian words and sentences inside given text.

    Args:
        text - Text that will be analyzed
    
    Returns:
        A dictionary containing  two keys with given values:
            - 'words': A list of singular Norwegian words found.
            - 'sentences': A list of Norwegian sentences found.
    """
    
    
    prompt = f"""
Jesteś asystentem który rozmawia tylko w JSON. Nie używaj zwykłego języka i nie dodawaj komentarzy, posługujesz się tylko JSON. Dostałeś następujące zadanie:
Podany tekst może zawierać fragmenty po norwesku i po polsku.
1. Wybierz wszystkie słowa norweskie bez powtórek i zapisz je w liście.
2. Wybierz wysztkie norweskie zdania jakie są i zapisz je w liście (pomijaj numery zdań jeżeli występują.)
3. Utwórz listę w JSON zawierającą wszystkie te słowa i zdania w podanym formacie:

{{'words': ['etter', 'at', ...], sentences: ['Eksempelsetning på norsk.', 'Ala har en katt.', ...]}},

Tekst do analizy:
{text}

"""

    # Limiting number of tokens weren't successful for now XD Don't know why
    response = ollama.chat(model="gpt-oss:20b", messages=[
        {"role": "user", "content": prompt}
    ],
    keep_alive=False)
    try:
        clean_json = re.sub(r"^```json\s*|\s*```$", "", response["message"]["content"].strip())
        data = json.loads(clean_json)
    except:
        print("Error during parsing to JSON. \nWiadomość:\n", response["message"]["content"])
        return "Error occured during analyzing text."
    
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

    # Straighten image for better ocr
    folder, image = os.path.split(image_path) # Format needed for straighten_image function
    straighten_image(folder, image)

    # Extract text
    straighten_image_path = straighten_img_path(folder, image) # Straighten image has new name
    ocr_model = ocr_predictor(det_arch="db_resnet50", reco_arch="crnn_mobilenet_v3_large", pretrained=True)
    doc = DocumentFile.from_images(straighten_image_path)
    return ocr_model(doc).render()


# Attempts to use only an LLM for accent correction resulted in missing words.
# Currently, all known "mistakes" (incorrect character mappings) are handled by replacement.
# In the future it will be handled differently
# Should be used just before saving to db (future) or presenting to user
# Lowers quality of LLM responses dramatically 
def clean_accents(word_list: List[str]) -> List[str]:
    """
    Cleans incorrect accents in Norwegian words within a list.

    Args:
        words: List of strings.
               Example: ['pâ', 'âr', 'Nâ']

    Returns:
        A new list with corrected accents in the words.
        Example: ['på', 'år', 'Nå']
    """
    corrected_list = []
    for word in word_list:
        corrected_word = word.replace('à', 'å') \
                             .replace('â', 'å') \
                             .replace('ä', 'æ') \
                             .replace('ö', 'ø') \
                             .replace('ò', 'ó') #

        corrected_list.append(corrected_word)

    return corrected_list

# For now its my handbook specific probably 
# Its implemented as such just to see how it works :)
# It will be changed in the future
def process_text(text: str) -> str:
    """
    
    """
    print("_"* 50)
    print(text) # Just "log" what is going on before 
    # Delete new lines and introduce them at the end of sentences
    text = text.replace("\n", "").replace(".", " \n ")

    # Delete /number/
    text = re.sub(r'/\d+/', '', text)

    # Delete all "/", "(" and replace ")" with " " 
    text = text.replace('/', '').replace('(', ''). replace(")", " ")
    
    print("_"* 50)
    print(text) # Just "log" what is going on after 
    return text



if __name__ == "__main__":
    test = "Cwiczenia 45 45.1 Polacz zdania spojnikiem ETTER AT. Uzyj czasow Przyklad Sonja spiste kvelds. Hun sovnet. phuskvamperfekeum i Etter at Sonja hadde spist kvelds, preteritum. sovnet hun. 1. Pappa banket pâ dora. Sonnen âpnet. 2. Vennene snakket sammen. De ringte hjem til sin kollega. 3. Martin fylte âr. Han tok sertifikat. 4. Monica leste ei bok. Hun gikk en tur. 5. Guttene sparket fotball. De kjopte sotsaker. 6. Per og Pâl kjopte godterier. De spiste dem. 7. Ola ringte. Luise grât. 8. Jeg jobbet mye. Jeg fikk vondti ryggen. 9. Tom rodde til Vika. Stormen begynte. 10. Deti regnet og blâste. Det lâ mange trari i gata. 45.2 Uzupelnij dialog czasownikami W czasie preteritum lub pluskvamperfelktum. Przyklad Han hadde reist til Hjerkinn. Sâ bodde han der 1 10 âr - Nâr /1/ (bli) du pensjonist? - Jeg /2/ (bli) pensjonist i fjor etter at jeg /3/ fabrikken i30 âr. (arbeide) pà - 14/ (fa) du en - Sjefen /5/ (kjope) avskjedsgave? ei klokke avskjedsfesten. og 16/ (snakke) lenge pâ -171 (veere) du ikke trist? - Ikkeidet hele tatt! Jeg/8/ (kysse) fabrikken for siste gang! Og jeg /10/ (spare) kontordama for jeg/9/ (ga) fra pâ jobben. Nâ vil reise en del penger for jeg /11/ (slutte) - Sâ heldig du er! jeg verden rundt!"
    print(analyze_text(test))

