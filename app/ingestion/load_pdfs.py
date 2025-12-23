from pathlib import Path
from app.core.config import settings


def list_pdf_paths() -> list[str]:
    pdf_dir = Path(settings.pdf_dir)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    return [str(p) for p in pdf_dir.glob("*.pdf")]
