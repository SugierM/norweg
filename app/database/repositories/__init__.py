from app.database.connection import db
from app.database.repositories.word_repository import WordRepository
from app.database.repositories.translation_repository import TranslationRepository


word_repo = WordRepository(db)
trnas_repo = TranslationRepository(db)