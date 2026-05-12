import argparse
import logging
from pathlib import Path

from csv_app.composition import build_application

def _resolve_jobs(pdf_path: Path, csv_path: Path) -> list[tuple[Path, Path]]:
    if not pdf_path.exists():
        raise SystemExit(f'No se encontró el PDF: {pdf_path}')

    if pdf_path.is_file():
        if pdf_path.suffix.lower() != '.pdf':
            raise SystemExit(f'El archivo de entrada no es un PDF: {pdf_path}')

        if csv_path.exists() and csv_path.is_dir():
            return [(pdf_path, csv_path / f'{pdf_path.stem}.csv')]

        if csv_path.suffix.lower() != '.csv':
            raise SystemExit(
                'La ruta de salida debe ser un archivo .csv o un directorio existente para un único PDF.'
            )
        return [(pdf_path, csv_path)]

    pdf_files = sorted(path for path in pdf_path.iterdir() if path.is_file() and path.suffix.lower() == '.pdf')
    if not pdf_files:
        raise SystemExit(f'No se encontraron archivos PDF en: {pdf_path}')

    if csv_path.exists() and not csv_path.is_dir():
        raise SystemExit('Cuando la entrada es un directorio, la salida debe ser un directorio.')
    if not csv_path.exists() and csv_path.suffix.lower() == '.csv':
        raise SystemExit('Cuando la entrada es un directorio, la salida no puede ser un archivo .csv.')

    csv_path.mkdir(parents=True, exist_ok=True)
    return [(pdf_file, csv_path / f'{pdf_file.stem}.csv') for pdf_file in pdf_files]


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Extrae texto y datos de gráficos de un PDF y los guarda en CSV.'
    )
    parser.add_argument('pdf_path', type=Path, help='Ruta al archivo PDF o a un directorio con PDFs.')
    parser.add_argument('csv_path', type=Path, help='Ruta al CSV de salida o a un directorio de salida.')
    parser.add_argument(
        '--poppler-path',
        type=str,
        default=None,
        help='Ruta a la carpeta bin de Poppler si no está en PATH (Windows).',
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    jobs = _resolve_jobs(args.pdf_path, args.csv_path)

    extractor, report_generator = build_application()
    for pdf_path, csv_path in jobs:
        logging.info('Extrayendo contenido del PDF: %s', pdf_path)
        pages = extractor.extract(pdf_path, poppler_path=args.poppler_path)
        logging.info('Generando CSV de salida: %s', csv_path)
        report_generator.generate(pages, csv_path, pdf_path=pdf_path)

    logging.info('Proceso completado. Archivos generados: %s', len(jobs))


if __name__ == '__main__':
    main()
