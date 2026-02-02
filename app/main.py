from fastapi import FastAPI

from app.config import settings
from app.db.session import check_db_connection

app = FastAPI(title=settings.app_name)

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