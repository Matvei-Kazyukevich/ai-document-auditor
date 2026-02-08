from time import sleep
from sqlalchemy.orm import Session

from app.db.crud.document import update_document, get_document_by_id
from app.api.schemas.document import DocumentUpdate
from app.db.models.document import DocumentStatus

# Demo document analyzer
def analyze_document(db: Session, document_id: int):
    document = get_document_by_id(db, document_id)
    if not document:
        return

    # uploaded -> processing
    update_document(db, document, DocumentUpdate(status=DocumentStatus.processing))

    sleep(1)

    # processing -> completed
    update_document(db, document, DocumentUpdate(status=DocumentStatus.completed))