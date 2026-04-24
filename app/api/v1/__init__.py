from fastapi import APIRouter
from . import routes_translations, wiki_

router = APIRouter()

router.include_router(routes_translations.router)
router.include_router(wiki_.router)