from setuptools import setup, find_packages

from dedop.version import __version__

packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

setup(
    name="dedop",
    version=__version__,
    description='Delay Doppler (Altimeter) Processor',
    license='GPL-3',
    author='DeDop Development Team',
    packages=packages,
    package_data={
        'dedop.ui.defaults': ['*.json', '*.txt'],
    },
    entry_points={
        'console_scripts': [
            'dedop = dedop.ui.cli:main'
        ]
    },
    # Requirements are not given here as we use a Conda environment
    # ,
    # install_requires=['numpy >= 1.9',
    #                  'netCDF4 >= 1.1',
    #                  'scipy',
    #                  'typing'],
    # extras_require={'dedop.ui': ['matplotlib >= 1.4', 'basemap >= 1.0.7']},
    # author_email='',
    # maintainer='',
    # maintainer_email='',
    # url='',
)
