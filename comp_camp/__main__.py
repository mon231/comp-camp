from sys import stderr
from pathlib import Path
from argparse import ArgumentParser

from .parser import parser
from .cpl_types import Program
from .quad_translator import QuadTranslator

CPL_FILE_SUFFIX = '.ou'
QUD_FILE_SUFFIX = '.qud'
AUTHOR_STUDENT_NAME = 'Ariel Tubul'


def cpl_to_quad(cpl_code: str) -> str:
    quad_translator = QuadTranslator()
    cpl_program: Program = parser.parse(cpl_code)

    quad_code = cpl_program.translate(quad_translator)
    return quad_code.opcodes


def parse_arguments():
    arguments_parser = ArgumentParser(f'{AUTHOR_STUDENT_NAME}\'s implementation for quad compiler')
    arguments_parser.add_argument('code_file', type=Path, help=f'Path to code-file (got to end with {CPL_FILE_SUFFIX})')
    arguments_parser.add_argument('--output', '-o', type=Path, required=False, help=f'Path to output file (recommended end with {QUD_FILE_SUFFIX})')
    return arguments_parser.parse_args()


def main():
    print(f'Running {AUTHOR_STUDENT_NAME}\'s compiler', file=stderr)

    arguments = parse_arguments()
    output_file: Path = arguments.output or arguments.code_file.with_suffix(QUD_FILE_SUFFIX)

    if not arguments.code_file.suffix == CPL_FILE_SUFFIX:
        raise RuntimeError(f'Unexpected suffix for input-file (should be "{CPL_FILE_SUFFIX}")')

    try:
        cpl_code = arguments.code_file.read_text()

        quad_code = cpl_to_quad(cpl_code)
        output_file.write_text(quad_code)
    except:
        output_file.unlink(missing_ok=True)
        raise


if __name__ == '__main__':
    main()
