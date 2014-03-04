import os
from setuptools import setup, find_packages

PACKAGE_DIR = 'src'

def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
    name = "selesame",
    version = '0.0.1',
    author = read('AUTHORS'),
    keywords = 'selenium',
    url = 'https://github.com/perfidia/selesame',
    data_files = [("", [PACKAGE_DIR + os.sep + 'selesame.py'])],
    long_description = read('README.md'),
    packages = find_packages(PACKAGE_DIR, exclude=['ez_setup', 'examples', 'tests']),
    zip_safe = False,
    classifiers = [
            'Environment :: Console',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2.7',
            'Topic :: Software Development :: Testing'
    ],
)
