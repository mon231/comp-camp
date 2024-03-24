import pytest
from pathlib import Path
from comp_camp.__main__ import cpl_to_quad, CPL_FILE_SUFFIX

SAMPLES_FOLDER = Path('samples')
SAMPLE_SOURCES = list(SAMPLES_FOLDER.glob(f'*{CPL_FILE_SUFFIX}'))


@pytest.mark.parametrize('sample_source_file', SAMPLE_SOURCES)
def test_file_compilation(sample_source_file: Path):
    cpl_to_quad(sample_source_file.read_text())
