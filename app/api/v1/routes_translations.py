from fastapi import APIRouter, HTTPException, Request
from app.services.translation_services import get_polish_from_norwegian

router = APIRouter()

@router.get("/translate/{word}")
def get_transaltion(word: str):
    word = word.strip().lower()
    result = get_polish_from_norwegian(word)

    return result