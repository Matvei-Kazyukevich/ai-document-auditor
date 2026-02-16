from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models.document import Document
from app.services.rules.runner import run_rules_for_document

def run_rules_background(document_id: int) -> None:
    db: Session = SessionLocal()

    try:
        document: Document | None = db.get(Document, document_id)
        if document is None:
            return
        run_rules_for_document(db, document)
    finally:
        db.close()