from __future__ import annotations

import enum
from datetime import datetime, UTC

from sqlalchemy import String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import AuditFinding
from app.db.models.base import Base
from app.db.models.rule import Rule
from app.db.models.document import Document

class RuleExecutionStatus(enum.Enum):
    running = 'running'
    passed = 'passed'
    failed = 'failed'

class RuleExecution(Base):
    __tablename__ = 'rule_executions'

    id: Mapped[int] = mapped_column(primary_key=True)
    rule_id: Mapped[int] = mapped_column(ForeignKey('rules.id', ondelete='CASCADE'), nullable=False, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey('documents.id', ondelete='CASCADE'), nullable=False, index=True)

    status: Mapped[RuleExecutionStatus] = mapped_column(
        Enum(RuleExecutionStatus),
        default=RuleExecutionStatus.running,
        nullable=False,
        index=True,
    )

    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    finished_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    rule: Mapped[Rule] = relationship(back_populates='executions')
    document: Mapped[Document] = relationship(back_populates='rule_executions')

    audit_findings: Mapped[AuditFinding] = relationship(
        back_populates='rule_execution',
        cascade='all, delete-orphan',
    )
