from pathlib import Path
from typing import Optional

from .entities import ExtractedPage
from .ports import (
    CsvExporterPort,
    GraphDataExtractorPort,
    MetadataExtractorPort,
    PdfImageConverterPort,
    PdfTextExtractorPort,
    StructureExtractorPort,
    TableExtractorPort,
)


class PdfContentExtractionService:
    def __init__(
        self,
        text_extractor: PdfTextExtractorPort,
        image_converter: PdfImageConverterPort,
        graph_extractor: GraphDataExtractorPort,
        table_extractor: TableExtractorPort,
        metadata_extractor: MetadataExtractorPort,
        structure_extractor: StructureExtractorPort,
    ) -> None:
        self.text_extractor = text_extractor
        self.image_converter = image_converter
        self.graph_extractor = graph_extractor
        self.table_extractor = table_extractor
        self.metadata_extractor = metadata_extractor
        self.structure_extractor = structure_extractor

    def extract(self, pdf_path: Path, poppler_path: Optional[str] = None) -> list[ExtractedPage]:
        text_blocks = self.text_extractor.extract_text(pdf_path)
        images = self.image_converter.convert_to_images(pdf_path, poppler_path=poppler_path)
        tables = self.table_extractor.extract_tables(pdf_path)
        structure = self.structure_extractor.extract_structure(pdf_path)

        extracted_pages: list[ExtractedPage] = []
        for text_block in text_blocks:
            image_index = text_block.page_number - 1
            graph_points = []
            if image_index < len(images):
                graph_points = self.graph_extractor.extract_points(images[image_index], text_block.page_number)
            
            page_tables = [t for t in tables if t.page_number == text_block.page_number]
            page_structure = [s for s in structure if s.page_number == text_block.page_number]
            
            extracted_pages.append(
                ExtractedPage(
                    page_number=text_block.page_number,
                    text_block=text_block,
                    graph_points=graph_points,
                    tables=page_tables,
                    structure=page_structure,
                )
            )
        return extracted_pages


class CsvReportGenerator:
    def __init__(self, exporter: CsvExporterPort, metadata_extractor: Optional[MetadataExtractorPort] = None) -> None:
        self.exporter = exporter
        self.metadata_extractor = metadata_extractor

    def generate(self, pages: list[ExtractedPage], output_path: Path, pdf_path: Optional[Path] = None) -> None:
        rows: list[dict] = []
        
        if self.metadata_extractor and pdf_path:
            metadata = self.metadata_extractor.extract_metadata(pdf_path)
            rows.append(
                {
                    "type": "metadata",
                    "page": "",
                    "graph_index": "",
                    "value": "",
                    "x": "",
                    "y": "",
                    "x_label": metadata.title or "",
                    "y_label": metadata.author or "",
                }
            )
        
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
            
            for structure in page.structure:
                rows.append(
                    {
                        "type": "structure",
                        "page": page.page_number,
                        "graph_index": "",
                        "value": structure.heading_text,
                        "x": structure.level,
                        "y": "",
                        "x_label": structure.content_type,
                        "y_label": "",
                    }
                )
            
            for table in page.tables:
                for row_index, row_data in enumerate(table.rows):
                    rows.append(
                        {
                            "type": "table",
                            "page": page.page_number,
                            "graph_index": table.table_index,
                            "value": "|".join(str(v) for v in row_data),
                            "x": row_index,
                            "y": "",
                            "x_label": "|".join(table.headers),
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
