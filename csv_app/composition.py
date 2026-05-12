from .adapters import GraphDataExtractor, PandasCsvExporter, PdfImageConverter, PdfTextExtractor
from .use_cases import CsvReportGenerator, PdfContentExtractionService


def build_application():
    text_extractor = PdfTextExtractor()
    image_converter = PdfImageConverter()
    graph_extractor = GraphDataExtractor()
    csv_exporter = PandasCsvExporter()

    content_service = PdfContentExtractionService(
        text_extractor=text_extractor,
        image_converter=image_converter,
        graph_extractor=graph_extractor,
    )
    report_generator = CsvReportGenerator(exporter=csv_exporter)
    return content_service, report_generator
