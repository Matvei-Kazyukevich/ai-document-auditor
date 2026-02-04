from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.schemas.document import DocumentCreate, DocumentUpdate
from app.db.models.document import Document

# Create and add new document in database
def create_document(db: Session, payload: DocumentCreate) -> Document:
    document = Document(
        original_filename=payload.original_filename,
        storage_path=payload.storage_path,
        content_type=payload.content_type,
        size_bytes=payload.size_bytes,
        sha256=payload.sha256,
    )

    db.add(document)
    db.commit()
    db.refresh(document)
    return document

# Get document from database by id
def get_document_by_id(db: Session, document_id: int) -> Document | None:
    query = select(Document).where(Document.id == document_id)
    return db.scalar(query)

# Update document from database (can update status, error_message, sha256)
def update_document(db: Session, document: Document, patch: DocumentUpdate) -> Document:
    if patch.status is not None:
        document.status = patch.status
    if patch.error_message is not None:
        document.error_message = patch.error_message
    if patch.sha256 is not None:
        document.sha256 = patch.sha256

    db.add(document)
    db.commit()
    db.refresh(document)
    return document