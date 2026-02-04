from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.db.session import check_db_connection, engine

from app.db.models import Base

from app.api.routers.document import router as documents_router

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)

@app.get('/health')
def health():
    db_check = check_db_connection()

    return {
        'status': 'ok',
        'app_name': settings.app_name,
        'env': settings.env,
        'database': settings.database_url,
        'database_connected': db_check,
    }

app.include_router(documents_router)