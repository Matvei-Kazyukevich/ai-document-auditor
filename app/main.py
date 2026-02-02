from fastapi import FastAPI
from app.config import settings

app = FastAPI(title=settings.app_name)

@app.get('/')
def start():
    return {
        'status': 'ok',
        'app_name': settings.app_name,
        'env': settings.env,
        'database': settings.database_url,
    }