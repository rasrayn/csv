from pathlib import Path
from typing import Optional

from .entities import ExtractedPage
from .ports import CsvExporterPort, GraphDataExtractorPort, PdfImageConverterPort, PdfTextExtractorPort


class PdfContentExtractionService:
    def __init__(
        self,
        text_extractor: PdfTextExtractorPort,
        image_converter: PdfImageConverterPort,
        graph_extractor: GraphDataExtractorPort,
    ) -> None:
        self.text_extractor = text_extractor
        self.image_converter = image_converter
        self.graph_extractor = graph_extractor

    def extract(self, pdf_path: Path, poppler_path: Optional[str] = None) -> list[ExtractedPage]:
        text_blocks = self.text_extractor.extract_text(pdf_path)
        images = self.image_converter.convert_to_images(pdf_path, poppler_path=poppler_path)

        extracted_pages: list[ExtractedPage] = []
        for text_block in text_blocks:
            image_index = text_block.page_number - 1
            graph_points = []
            if image_index < len(images):
                graph_points = self.graph_extractor.extract_points(images[image_index], text_block.page_number)
            extracted_pages.append(
                ExtractedPage(
                    page_number=text_block.page_number,
                    text_block=text_block,
                    graph_points=graph_points,
                )
            )
        return extracted_pages


class CsvReportGenerator:
    def __init__(self, exporter: CsvExporterPort) -> None:
        self.exporter = exporter

    def generate(self, pages: list[ExtractedPage], output_path: Path) -> None:
        rows: list[dict] = []
        for page in pages:
            rows.append(
                {
                    "type": "text",
                    "page": page.page_number,
                    "graph_index": "",
                    "value": page.text_block.text,
                    "x": "",
                    "y": "",
                    "x_label": "",
                    "y_label": "",
                }
            )
            for point in page.graph_points:
                rows.append(
                    {
                        "type": "graph_point",
                        "page": page.page_number,
                        "graph_index": point.graph_index,
                        "value": "",
                        "x": point.x,
                        "y": point.y,
                        "x_label": point.x_label or "",
                        "y_label": point.y_label or "",
                    }
                )
        self.exporter.export(rows, output_path)
