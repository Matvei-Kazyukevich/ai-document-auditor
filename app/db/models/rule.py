from __future__ import annotations

import enum
from datetime import datetime, UTC

from sqlalchemy import String, Boolean, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.rule_execution import RuleExecution

class RuleSeverity(enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class Rule(Base):
    __tablename__ = 'rules'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)

    severity: Mapped[RuleSeverity] = mapped_column(
        Enum(RuleSeverity),
        default=RuleSeverity.low,
        nullable=False,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

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

    executions: Mapped[list[RuleExecution]] = relationship(back_populates='rule', cascade='all, delete-orphan')


