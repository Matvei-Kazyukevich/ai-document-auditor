from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.models import Document
from app.deps import get_db
from app.api.schemas.document import DocumentCreate, DocumentRead, DocumentUpdate
from app.db.crud.document import create_document, get_document_by_id, update_document
from app.services.storage.local_storage import save_file
from app.services.analysis.document_analyzer import analyze_document
from app.services.rules.tasks import run_rules_background

router = APIRouter(prefix="/documents", tags=["documents"])

# Router for create document
@router.post('', response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create(payload: DocumentCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    document = create_document(db, payload)

    background_tasks.add_task(run_rules_background, document.id)
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

# Router for upload document
@router.post('/upload', response_model=DocumentRead, status_code=201)
def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save document and read size, SHA256
    storage_path, size_bytes, sha256_hash = save_file(file)

    # Check for duplicate
    existing_document = db.query(Document).filter(Document.sha256 == sha256_hash).first()
    if existing_document:
        return DocumentRead.model_validate(existing_document)

    # Create document
    payload = DocumentCreate(
        original_filename=file.filename,
        storage_path=storage_path,
        content_type=file.content_type,
        size_bytes=size_bytes,
        sha256=sha256_hash,
    )
    document = create_document(db, payload)

    # Analyze document
    background_tasks.add_task(analyze_document, db=db, document_id=document.id)

    return DocumentRead.model_validate(document)
