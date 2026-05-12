from pathlib import Path
from typing import Protocol
from PIL.Image import Image

from .entities import GraphPoint, Table, TextBlock, DocumentMetadata, DocumentStructure

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

class TableExtractorPort(Protocol):
    def extract_tables(self, pdf_path: Path) -> list[Table]:
        ...

class MetadataExtractorPort(Protocol):
    def extract_metadata(self, pdf_path: Path) -> DocumentMetadata:
        ...

class StructureExtractorPort(Protocol):
    def extract_structure(self, pdf_path: Path) -> list[DocumentStructure]:
        ...
