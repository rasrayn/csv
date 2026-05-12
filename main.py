import argparse
import logging
from pathlib import Path

from csv_app.composition import build_application


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Extrae texto y datos de gráficos de un PDF y los guarda en CSV.'
    )
    parser.add_argument('pdf_path', type=Path, help='Ruta al archivo PDF de entrada.')
    parser.add_argument('csv_path', type=Path, help='Ruta al archivo CSV de salida.')
    parser.add_argument(
        '--poppler-path',
        type=str,
        default=None,
        help='Ruta a la carpeta bin de Poppler si no está en PATH (Windows).',
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    if not args.pdf_path.exists():
        raise SystemExit(f'No se encontró el PDF: {args.pdf_path}')

    extractor, report_generator = build_application()
    logging.info('Extrayendo contenido del PDF...')
    pages = extractor.extract(args.pdf_path, poppler_path=args.poppler_path)
    logging.info('Generando CSV de salida...')
    report_generator.generate(pages, args.csv_path, pdf_path=args.pdf_path)
    logging.info('CSV generado en %s', args.csv_path)


if __name__ == '__main__':
    main()
