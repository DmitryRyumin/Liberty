import sys

from setuptools import setup, find_packages

MIN_PYTHON_VERSION = (3, 7)

if sys.version_info[:2] < MIN_PYTHON_VERSION:
    raise RuntimeError('Python version required = {}.{}'.format(MIN_PYTHON_VERSION[0], MIN_PYTHON_VERSION[1]))

import liberty

REQUIRED_PACKAGES = [
    'numpy >= 1.18.5',
    'opencv-contrib-python >= 4.4.0.42',
    'PyOpenGL >= 3.1.5',
    'PyOpenGL-accelerate >= 3.1.5',
    'Pillow >= 8.0.0',
    'comtypes >= 1.1.7',
    'colorama >= 0.4.3',
    'xmltodict >= 0.12.0'
]

CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Natural Language :: Russian
Natural Language :: English
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Mathematics
Topic :: Software Development
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX :: Linux
"""

with open('README.md', 'r') as fh:
    long_description = fh.read()

    setup(
        name = liberty.__name__,
        packages = find_packages(),
        license = liberty.__license__,
        version = liberty.__version__,
        author = liberty.__author__,
        author_email = liberty.__email__,
        maintainer = liberty.__maintainer__,
        maintainer_email = liberty.__maintainer_email__,
        url = liberty.__uri__,
        description = liberty.__summary__,
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        install_requires=REQUIRED_PACKAGES,
        keywords = ['liberty'],
        include_package_data = True,
        classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f],
        python_requires = '>=3.7',
        entry_points = {
            'console_scripts': [
                'liberty_play = liberty.samples.play:main',
                'liberty_facesdet = liberty.samples.facesdet_play:main',
            ],
        },
    )
