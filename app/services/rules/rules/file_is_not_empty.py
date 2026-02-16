from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.rules.base import BaseRule
from app.db.models.document import Document
from app.db.models.audit_finding import AuditFinding, AuditSeverity, RiskType

class FileIsNotEmptyRule(BaseRule):
    code = 'FILE_001'
    name = 'File Is Not Empty'
    description = 'Check if a document is empty'
    risk_type = RiskType.logic_error
    severity = AuditSeverity.high

    def run(self, db: Session, document: Document) -> list[AuditFinding]:
        findings: list[AuditFinding] = []

        if document.size_bytes == 0:
            findings.append(
                AuditFinding(
                    severity=self.severity,
                    risk_type=self.risk_type,
                    title='Empty file',
                    description=(
                        f'File {document.original_filename} is empty.'
                    ),
                    recommendation=(
                        'Check uploading file and repeat.'
                    ),
                )
            )

        return findings