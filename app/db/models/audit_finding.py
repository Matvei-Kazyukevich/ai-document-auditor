from __future__ import annotations

import enum
from datetime import datetime,UTC

from sqlalchemy import String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.document import Document
from app.db.models.rule_execution import RuleExecution

class AuditSeverity(enum.Enum):
     low = 'low'
     medium = 'medium'
     high = 'high'

class RiskType(enum.Enum):
    duplicate = 'duplicate'
    overflow = 'overflow'
    mismatch = 'mismatch'
    anomaly = 'anomaly'
    logic_error = 'logic_error'

class AuditFinding(Base):
    __tablename__ = 'audit_findings'

    id: Mapped[int] = mapped_column(primary_key=True)

    document_id: Mapped[int] = mapped_column(
        ForeignKey('documents.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )

    rule_execution_id: Mapped[int] = mapped_column(
        ForeignKey('rule_executions.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )

    severity: Mapped[AuditSeverity] = mapped_column(
        Enum(AuditSeverity),
        default=AuditSeverity.low,
        nullable=False,
        index=True,
    )

    risk_type: Mapped[RiskType] = mapped_column(
        Enum(RiskType),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=False)
    recommendation: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    document: Mapped[Document] = relationship()
    rule_execution: Mapped[RuleExecution] = relationship()