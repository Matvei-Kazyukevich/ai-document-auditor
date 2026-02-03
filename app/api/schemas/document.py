from __future__ import annotations

from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.db.models.document import DocumentStatus

FileNameStr = Annotated[str, Field(min_length=1, max_length=255)]
StoragePathStr = Annotated[str, Field(min_length=1, max_length=512)]
ContentTypeStr = Annotated[str, Field(min_length=1, max_length=100)]
SizeBytesInt = Annotated[int, Field(ge=0)]
Sha256Str = Annotated[str, Field(min_length=64, max_length=64, description='Lowercase hex sha256')]
ErrorMessageStr = Annotated[str, Field(max_length=1000)]


class DocumentBase(BaseModel):
    original_filename: FileNameStr
    storage_path: StoragePathStr
    content_type: ContentTypeStr
    size_bytes: SizeBytesInt
    sha256: Optional[Sha256Str] = None

    @field_validator('storage_path')
    @classmethod
    def validate_storage_path(cls, value: str) -> str:
        value = value.strip()
        if value.startswith('/') or ':\\' in value or ':/' in value:
            raise ValueError('storage_path must be a relative storage key, not an absolute OS path')
        if '..' in value:
            raise ValueError('storage_path must not contain ".."')
        return value

    @field_validator('sha256')
    @classmethod
    def validate_sha256(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value_low = value.strip().lower()
        allowed = set('0123456789abcdef')
        if any(char not in allowed for char in value_low):
            raise ValueError('sha256 must contain only lowercase hex digits')
        return value_low

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    status: Optional[DocumentStatus] = None
    error_message: Optional[ErrorMessageStr] = None
    sha256: Optional[Sha256Str] = None

    @field_validator('sha256')
    @classmethod
    def validate_sha256(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value_low = value.strip().lower()
        allowed = set('0123456789abcdef')
        if any(char not in allowed for char in value_low):
            raise ValueError('sha256 must contain only lowercase hex digits')
        return value_low

class DocumentRead(DocumentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: DocumentStatus
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

