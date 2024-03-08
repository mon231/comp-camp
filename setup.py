import setuptools
from pathlib import Path

CURRENT_FOLDER = Path(__file__).parent
README_PATH = CURRENT_FOLDER / 'README.md'


setuptools.setup(
    name = "comp_camp",
    version = "1.0.0",
    author = "Ariel Tubul",
    install_requires = ['ply'],
    packages = setuptools.find_packages(),
    long_description=README_PATH.read_text(),
    long_description_content_type='text/markdown',
    url = "https://github.com/mon231/comp-camp/",
    description = "",
    entry_points = {'console_scripts': ['cpq=comp_camp.__main__:main']}
)
