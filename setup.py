from setuptools import setup, find_packages

packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

setup(
    name="dedop",
    version="0.1.0",
    description='Delay Doppler (Altimeter) Processor',
    license='GPL 3',
    author='DeDop Development Team',
    packages=packages,
    package_data={
        'dedop.cli.defaults': ['*.json', '*.txt'],
    },
    entry_points={
        'console_scripts': [
            'dedop = dedop.cli:main'
        ]
    }
    # Requirements are not given here as we use a Conda environment
    # ,
    # install_requires=['numpy >= 1.9',
    #                  'netCDF4 >= 1.1',
    #                  'scipy',
    #                  'typing'],
    # extras_require={'dedop.cli': ['matplotlib >= 1.4', 'basemap >= 1.0.7']},
    # author_email='',
    # maintainer='',
    # maintainer_email='',
    # url='',
)
