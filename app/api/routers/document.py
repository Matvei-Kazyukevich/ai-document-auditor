from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.api.schemas.document import DocumentCreate, DocumentRead, DocumentUpdate
from app.db.crud.document import create_document, get_document_by_id, update_document

router = APIRouter(prefix="/documents", tags=["documents"])

# Router for create document
@router.post('', response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create(payload: DocumentCreate, db: Session = Depends(get_db)):
    document = create_document(db, payload)
    return DocumentRead.model_validate(document)

# Router for get document by id
@router.get('/{document_id}', response_model=DocumentRead)
def get(document_id: int, db: Session = Depends(get_db)):
    document = get_document_by_id(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentRead.model_validate(document)

# Router for update document
@router.patch('/{document_id}', response_model=DocumentRead)
def patch(document_id: int, payload: DocumentUpdate, db: Session = Depends(get_db)):
    document = get_document_by_id(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    document = update_document(db, document, payload)
    return DocumentRead.model_validate(document)
