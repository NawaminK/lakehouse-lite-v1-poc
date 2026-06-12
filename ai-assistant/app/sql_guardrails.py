import re

BLOCKED_KEYWORDS = [
    "drop",
    "delete",
    "insert",
    "update",
    "alter",
    "create",
    "truncate",
    "merge",
    "call",
    "grant",
    "revoke",
]


class SqlValidationError(ValueError):
    """Raised when a SQL statement violates the POC read-only policy."""


def normalize_sql(sql: str) -> str:
    return re.sub(r"\s+", " ", sql.strip())


def validate_sql(sql: str) -> str:
    normalized = normalize_sql(sql)
    lowered = normalized.lower()

    if not normalized:
        raise SqlValidationError("SQL statement is required")

    if re.search(r"(--|/\*|\*/)", normalized):
        raise SqlValidationError("SQL comments are not allowed in the POC query API")

    if normalized.endswith(";"):
        normalized = normalized[:-1].strip()
        lowered = normalized.lower()

    if ";" in normalized:
        raise SqlValidationError("Multiple SQL statements are not allowed")

    if not re.match(r"^(select|show)\b", lowered):
        raise SqlValidationError("Only SELECT and SHOW statements are allowed")

    for keyword in BLOCKED_KEYWORDS:
        if re.search(rf"\b{keyword}\b", lowered):
            raise SqlValidationError(f"Blocked SQL keyword: {keyword}")

    return normalized

