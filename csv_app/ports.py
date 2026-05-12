from pathlib import Path
from typing import Protocol
from PIL.Image import Image

from .entities import GraphPoint, TextBlock

class PdfTextExtractorPort(Protocol):
    def extract_text(self, pdf_path: Path) -> list[TextBlock]:
        ...

class PdfImageConverterPort(Protocol):
    def convert_to_images(self, pdf_path: Path, poppler_path: str | None = None) -> list[Image]:
        ...

class GraphDataExtractorPort(Protocol):
    def extract_points(self, image: Image, page_number: int) -> list[GraphPoint]:
        ...

class CsvExporterPort(Protocol):
    def export(self, rows: list[dict], output_path: Path) -> None:
        ...
