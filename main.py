from pathlib import Path
from argparse import ArgumentParser
from tokenizer import create_token_stream

CPL_FILE_SUFFIX = '.ou'
QUD_FILE_SUFFIX = '.qud'


def parse_arguments():
    arguments_parser = ArgumentParser('Ariel Tubul\'s implementation for quad compiler')
    arguments_parser.add_argument('code_file', type=Path, help=f'Path to code-file (got to end with {CPL_FILE_SUFFIX})')
    arguments_parser.add_argument('--output', '-o', type=Path, required=False, help=f'Path to output file (recommended end with {QUD_FILE_SUFFIX})')
    return arguments_parser.parse_args()


def main():
    arguments = parse_arguments()
    output_file: Path = arguments.output or arguments.code_file.with_suffix(QUD_FILE_SUFFIX)

    if not arguments.code_file.suffix == CPL_FILE_SUFFIX:
        raise RuntimeError(f'Unexpected suffix for input-file (should be "{CPL_FILE_SUFFIX}")')

    try:
        token_stream = create_token_stream(arguments.code_file.read_text())
        for tok in token_stream:
            print(tok)
    except:
        output_file.unlink(missing_ok=True)
        raise


if __name__ == '__main__':
    main()
