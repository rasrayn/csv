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
class ExtractedPage:
    page_number: int
    text_block: TextBlock
    graph_points: list[GraphPoint]
