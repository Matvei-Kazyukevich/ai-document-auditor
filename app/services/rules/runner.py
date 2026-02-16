from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy.orm import Session

from app.db.models.document import Document
from app.db.models.rule import Rule
from app.db.models.rule_execution import RuleExecution, RuleExecutionStatus
from app.db.models.audit_finding import AuditFinding

from app.services.rules.registry import get_all_rules


def run_rules_for_document(db: Session, document: Document) -> None:
    rules = get_all_rules()

    for rule_impl in rules:
        rule: Optional[Rule] = (
            db.query(Rule)
            .filter(Rule.code == rule_impl.code, Rule.is_active.is_(True))
            .one_or_none()
        )

        if not rule:
            continue

        execution = RuleExecution(
            rule=rule,
            document=document,
            status=RuleExecutionStatus.running,
        )

        db.add(execution)
        db.commit()
        db.refresh(execution)

        try:
            findings = rule_impl.run(db=db, document=document)

            for finding in findings:
                finding.document = document
                finding.rule_execution = execution
                db.add(finding)

            execution.status = RuleExecutionStatus.passed

        except Exception as e:
            execution.status = RuleExecutionStatus.failed
            execution.error_message = str(e)

        db.commit()