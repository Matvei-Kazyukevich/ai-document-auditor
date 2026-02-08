import hashlib
from pathlib import Path
from fastapi import UploadFile
from app.config import settings

UPLOAD_DIR = Path(settings.storage_dir) / "documents" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Save file and read SHA256
# Return path to document, size and SHA256
def save_file(file: UploadFile) -> tuple[str, int, str]:
    safe_path = UPLOAD_DIR / file.filename

    content = file.file.read()
    sha256_hash = hashlib.sha256(content).hexdigest()
    safe_path.write_bytes(content)

    size = len(content)
    relative_path = safe_path.relative_to(Path(settings.storage_dir))
    return str(relative_path), size, sha256_hash
