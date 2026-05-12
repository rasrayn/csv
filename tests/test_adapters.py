from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw

import csv_app.adapters as adapters
from csv_app.adapters import GraphDataExtractor, PandasCsvExporter


def test_pandas_csv_exporter_writes_csv(tmp_path: Path) -> None:
    rows = [
        {"type": "text", "page": 1, "graph_index": "", "value": "Hola", "x": "", "y": "", "x_label": "", "y_label": ""},
        {"type": "graph_point", "page": 1, "graph_index": 1, "value": "", "x": 10.0, "y": 20.0, "x_label": "X", "y_label": "Y"},
    ]
    output_path = tmp_path / "output.csv"

    PandasCsvExporter().export(rows, output_path)

    df = pd.read_csv(output_path)
    assert list(df.columns) == ["type", "page", "graph_index", "value", "x", "y", "x_label", "y_label"]
    assert df.iloc[0]["type"] == "text"
    assert df.iloc[1]["x_label"] == "X"


def test_graph_data_extractor_detects_points_and_labels(monkeypatch: object) -> None:
    image = Image.new("RGB", (300, 220), "white")
    draw = ImageDraw.Draw(image)
    draw.text((10, 190), "EjeX", fill="black")
    draw.text((0, 10), "EjeY", fill="black")

    circle_centers = [(70, 130), (140, 100), (210, 140)]
    for x, y in circle_centers:
        draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill="black")

    monkeypatch.setattr(adapters, "_ocr_text", lambda image, config="": "LABEL")

    extractor = GraphDataExtractor()
    points = extractor.extract_points(image, page_number=1)

    assert len(points) == len(circle_centers)
    assert points[0].x < points[1].x < points[2].x
    assert points[0].x_label == "LABEL"
    assert points[0].y_label == "LABEL"
