from __future__ import annotations

from typing import Iterable

from app.services.rules.base import BaseRule
from app.services.rules.rules.file_is_not_empty import FileIsNotEmptyRule


def get_all_rules() -> Iterable[BaseRule]:
    return [
        FileIsNotEmptyRule(),
    ]