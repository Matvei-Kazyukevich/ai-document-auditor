from __future__ import annotations

from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from app.db.models.document import Document
from app.db.models.audit_finding import AuditFinding, AuditSeverity, RiskType

class BaseRule(ABC):
    code: str
    name: str
    description: str
    risk_type: RiskType
    severity: AuditSeverity

    def run(self, db: Session, document: Document) -> list[AuditFinding]:
        """

        Run rule
        Return list of finding risks
        """
        