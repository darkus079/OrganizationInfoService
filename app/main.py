from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "REST API справочника организаций, зданий и деятельностей. "
        "Доступ к методам защищен статическим API-ключом в заголовке X-API-Key."
    ),
    version="1.0.0",
)
app.include_router(api_router, prefix=settings.api_v1_prefix)
