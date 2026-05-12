from pathlib import Path

from csv_app.entities import ExtractedPage, GraphPoint, TextBlock
from csv_app.use_cases import CsvReportGenerator, PdfContentExtractionService


class StubTextExtractor:
    def extract_text(self, pdf_path: Path) -> list[TextBlock]:
        return [TextBlock(page_number=1, text="Hola"), TextBlock(page_number=2, text="Mundo")]


class StubImageConverter:
    def convert_to_images(self, pdf_path: Path, poppler_path: str | None = None) -> list[str]:
        return ["img1", "img2"]


class StubGraphExtractor:
    def __init__(self) -> None:
        self.calls = []

    def extract_points(self, image: str, page_number: int) -> list[GraphPoint]:
        self.calls.append((image, page_number))
        return [GraphPoint(page_number=page_number, graph_index=1, x=10.0, y=20.0)]


class StubExporter:
    def __init__(self) -> None:
        self.rows = []
        self.last_path = None

    def export(self, rows: list[dict], output_path: Path) -> None:
        self.rows = rows
        self.last_path = output_path


def test_pdf_content_extraction_service_combines_text_and_graphs() -> None:
    extractor = PdfContentExtractionService(
        text_extractor=StubTextExtractor(),
        image_converter=StubImageConverter(),
        graph_extractor=StubGraphExtractor(),
    )
    pages = extractor.extract(Path("dummy.pdf"))

    assert len(pages) == 2
    assert pages[0].text_block.text == "Hola"
    assert pages[0].graph_points[0].x == 10.0
    assert pages[1].text_block.text == "Mundo"
    assert pages[1].graph_points[0].y == 20.0


def test_csv_report_generator_outputs_text_and_graph_rows(tmp_path: Path) -> None:
    page = ExtractedPage(
        page_number=1,
        text_block=TextBlock(page_number=1, text="Texto de prueba"),
        graph_points=[GraphPoint(page_number=1, graph_index=1, x=12.34, y=56.78, x_label="X", y_label="Y")],
    )
    exporter = StubExporter()
    report_generator = CsvReportGenerator(exporter=exporter)

    report_generator.generate([page], output_path=tmp_path / "output.csv")

    assert exporter.last_path == tmp_path / "output.csv"
    assert exporter.rows[0]["type"] == "text"
    assert exporter.rows[0]["value"] == "Texto de prueba"
    assert exporter.rows[1]["type"] == "graph_point"
    assert exporter.rows[1]["x"] == 12.34
    assert exporter.rows[1]["y_label"] == "Y"
