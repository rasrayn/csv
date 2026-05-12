from pathlib import Path

import pytest

from main import _resolve_jobs


def test_resolve_jobs_directory_input_and_output(tmp_path: Path) -> None:
    pdf_dir = tmp_path / "pdf"
    csv_dir = tmp_path / "salida"
    pdf_dir.mkdir()
    (pdf_dir / "a.pdf").write_bytes(b"%PDF-1.4")
    (pdf_dir / "b.PDF").write_bytes(b"%PDF-1.4")

    jobs = _resolve_jobs(pdf_dir, csv_dir)

    assert csv_dir.exists()
    assert csv_dir.is_dir()
    assert len(jobs) == 2
    assert [pdf.name for pdf, _ in jobs] == ["a.pdf", "b.PDF"]
    assert [csv.name for _, csv in jobs] == ["a.csv", "b.csv"]


def test_resolve_jobs_directory_input_rejects_csv_file_output(tmp_path: Path) -> None:
    pdf_dir = tmp_path / "pdf"
    pdf_dir.mkdir()
    (pdf_dir / "a.pdf").write_bytes(b"%PDF-1.4")
    output_csv_file = tmp_path / "salida.csv"

    with pytest.raises(SystemExit):
        _resolve_jobs(pdf_dir, output_csv_file)
