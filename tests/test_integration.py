import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest
from reportlab.pdfgen.canvas import Canvas


def _create_sample_pdf(pdf_path: Path) -> None:
    canvas = Canvas(str(pdf_path))
    canvas.drawString(100, 750, "Texto de prueba")
    canvas.drawString(50, 100, "EjeX")
    canvas.drawString(10, 400, "EjeY")
    canvas.setFillColorRGB(0, 0, 0)
    for x, y in [(120, 520), (170, 500), (220, 540)]:
        canvas.circle(x, y, 8, fill=1)
    canvas.showPage()
    canvas.save()


def test_cli_process_pdf_to_csv(tmp_path: Path) -> None:
    pdftoppm_bin = shutil.which("pdftoppm")
    poppler_bin_path = r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin"
    
    if pdftoppm_bin is None:
        if not Path(poppler_bin_path).exists():
            pytest.skip("Poppler no encontrado ni en PATH ni en ruta conocida")
        poppler_path = poppler_bin_path
    else:
        poppler_path = str(Path(pdftoppm_bin).parent)

    root = Path(__file__).resolve().parents[1]
    main_script = root / "main.py"
    pdf_path = tmp_path / "sample.pdf"
    csv_path = tmp_path / "output.csv"

    _create_sample_pdf(pdf_path)

    completed = subprocess.run(
        [sys.executable, str(main_script), str(pdf_path), str(csv_path), "--poppler-path", poppler_path],
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert csv_path.exists()

    df = pd.read_csv(csv_path)
    assert "type" in df.columns
    text_value = df.loc[df["type"] == "text", "value"].iloc[0]
    assert "Texto de prueba" in text_value
    assert len(df.loc[df["type"] == "graph_point"]) >= 1
