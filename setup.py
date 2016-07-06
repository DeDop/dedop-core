from setuptools import setup

setup(
    name="dedop",
    version="0.1.0",
    description='Delay Doppler (Altimeter) Processor',
    license='GPL 3',
    author='DeDop Development Team',
    packages=['dedop.model',
              'dedop.proc',
              'dedop.conf',
              'dedop.util',
              'dedop.cli'],
    entry_points={
        'console_scripts': [
            'dedop = dedop.cli:main'
        ]
    } # ,
    #install_requires=['numpy >= 1.9',
    #                  'netCDF4 >= 1.1',
    #                  'scipy',
    #                  'typing'],
    #extras_require={'dedop.cli': ['matplotlib >= 1.4', 'basemap >= 1.0.7']},
    # author_email='',
    # maintainer='',
    # maintainer_email='',
    # url='',
)
