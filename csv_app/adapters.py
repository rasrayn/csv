import csv
import shutil
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

TESSERACT_AVAILABLE = shutil.which("tesseract") is not None

from .entities import GraphPoint, TextBlock


class PdfTextExtractor:
    def extract_text(self, pdf_path: Path) -> list[TextBlock]:
        text_pages: list[TextBlock] = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                text_pages.append(TextBlock(page_number=page_number, text=text.strip()))
        return text_pages


class PdfImageConverter:
    def convert_to_images(self, pdf_path: Path, poppler_path: str | None = None) -> list[Image]:
        return convert_from_path(str(pdf_path), dpi=200, poppler_path=poppler_path)


def _pil_to_cv2(image: Image) -> np.ndarray:
    return cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)


def _ocr_text(image: np.ndarray, config: str = "--psm 6") -> str:
    if not TESSERACT_AVAILABLE:
        return ""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    raw_text = pytesseract.image_to_string(thresh, config=config)
    return " ".join(raw_text.split())


def _extract_axis_label(image: np.ndarray, axis: str) -> str | None:
    height, width = image.shape[:2]
    if axis == "x":
        roi = image[int(height * 0.82) : height, 0:width]
    else:
        roi = image[0:height, 0:int(width * 0.18)]
    text = _ocr_text(roi)
    return text or None


def _detect_graph_points(image: np.ndarray) -> list[tuple[float, float]]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    points: list[tuple[float, float]] = []
    height, width = gray.shape
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 20 or area > width * height * 0.15:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        points.append((float(x + w / 2), float(y + h / 2)))
    points.sort(key=lambda point: point[0])
    return points


class GraphDataExtractor:
    def extract_points(self, image: Image, page_number: int) -> list[GraphPoint]:
        cv_image = _pil_to_cv2(image)
        points = _detect_graph_points(cv_image)
        x_label = _extract_axis_label(cv_image, "x")
        y_label = _extract_axis_label(cv_image, "y")

        graph_points: list[GraphPoint] = []
        for graph_index, (x, y) in enumerate(points, start=1):
            graph_points.append(
                GraphPoint(
                    page_number=page_number,
                    graph_index=graph_index,
                    x=round(x, 2),
                    y=round(y, 2),
                    x_label=x_label,
                    y_label=y_label,
                )
            )
        return graph_points


class PandasCsvExporter:
    def export(self, rows: list[dict], output_path: Path) -> None:
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False, quoting=csv.QUOTE_MINIMAL)
