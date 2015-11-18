from setuptools import setup

setup(
    name="dedop",
    version="0.1.0",
    description='Delay Doppler (Altimeter) Processor',
    license='GPL 3',
    author='DeDop Development Team',
    packages=['dedop.model',
              'dedop.io',
              'dedop.proc',
              'dedop.conf',
              'dedop.util',
              'dedop.cli',
              'dedop.gui'],
    entry_points={
        'console_scripts': [
            'dedop-cli = dedop.cli.main:main',
            'dedop-gui = dedop.gui.main:main',
        ]
    },
    install_requires=['numpy >= 1.9',
                      'netCDF4 >= 1.1',
                      'scipy'],
    extras_require={'dedop.gui': ['PyQt5 >= 5.5', 'matplotlib >= 1.4']},
    # author_email='',
    # maintainer='',
    # maintainer_email='',
    # url='',
)
