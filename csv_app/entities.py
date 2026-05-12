from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class TextBlock:
    page_number: int
    text: str

@dataclass(frozen=True)
class GraphPoint:
    page_number: int
    graph_index: int
    x: float
    y: float
    x_label: Optional[str] = None
    y_label: Optional[str] = None

@dataclass(frozen=True)
class Table:
    page_number: int
    table_index: int
    headers: list[str]
    rows: list[list[str]]

@dataclass(frozen=True)
class DocumentMetadata:
    title: Optional[str] = None
    author: Optional[str] = None
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None

@dataclass(frozen=True)
class DocumentStructure:
    page_number: int
    level: int
    heading_text: str
    content_type: str

@dataclass(frozen=True)
class ExtractedPage:
    page_number: int
    text_block: TextBlock
    graph_points: list[GraphPoint]
    tables: list[Table]
    structure: list[DocumentStructure]
