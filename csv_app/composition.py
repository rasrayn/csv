from .adapters import (
    GraphDataExtractor,
    MetadataExtractor,
    PandasCsvExporter,
    PdfImageConverter,
    PdfTextExtractor,
    StructureExtractor,
    TableExtractor,
)
from .use_cases import CsvReportGenerator, PdfContentExtractionService


def build_application():
    text_extractor = PdfTextExtractor()
    image_converter = PdfImageConverter()
    graph_extractor = GraphDataExtractor()
    csv_exporter = PandasCsvExporter()
    table_extractor = TableExtractor()
    metadata_extractor = MetadataExtractor()
    structure_extractor = StructureExtractor()

    content_service = PdfContentExtractionService(
        text_extractor=text_extractor,
        image_converter=image_converter,
        graph_extractor=graph_extractor,
        table_extractor=table_extractor,
        metadata_extractor=metadata_extractor,
        structure_extractor=structure_extractor,
    )
    report_generator = CsvReportGenerator(exporter=csv_exporter, metadata_extractor=metadata_extractor)
    return content_service, report_generator
