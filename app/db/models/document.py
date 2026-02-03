import enum
from datetime import datetime, UTC

from sqlalchemy import String, DateTime, Enum, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class DocumentStatus(enum.Enum):
    uploaded = "uploaded"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)

    # File name from user
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)

    # File path/key in storage
    storage_path: Mapped[str] = mapped_column(String(512), nullable=False)

    # MIME type: application/pdf, text/plain, etc.
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)

    # File size in bytes
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # Optional file hash (lowercase hex sha256, 64 chars)
    sha256: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)

    # File status
    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus),
        default=DocumentStatus.uploaded,
        nullable=False,
        index=True,
    )

    # Error details if processing failed
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )