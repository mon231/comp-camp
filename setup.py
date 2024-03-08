import setuptools
from typing import List
from pathlib import Path


CURRENT_FOLDER = Path(__file__).parent
README_PATH = CURRENT_FOLDER / 'README.md'


def get_requirements() -> List[str]:
    REQUIREMENTS_FILE_NAME = 'requirements.txt'
    requirements_path = CURRENT_FOLDER / REQUIREMENTS_FILE_NAME

    requirements_content = requirements_path.read_text()
    return [requirement for requirement in requirements_content.splitlines() if requirement]


setuptools.setup(
    name = "comp_camp",
    version = "1.0.0",
    author = "Ariel Tubul",
    install_requires = get_requirements(),
    packages = setuptools.find_packages(),
    long_description=README_PATH.read_text(),
    long_description_content_type='text/markdown',
    url = "https://github.com/mon231/comp-camp/",
    description = "",
    entry_points = {'console_scripts': ['cpq=comp_camp.__main__:main']}
)
