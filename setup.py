from setuptools import setup

setup(
    name="dedop",
    version="0.1.0",
    description='Delay Doppler (Altimeter) Processor',
    license='GPL 3',
    author='DeDop Development Team',
    packages=['dedop.core',
              'dedop.io',
              'dedop.proc',
              'dedop.cli',
              'dedop.gui'],
    entry_points={
        'console_scripts': [
            'dedop_cli = dedop.cli.__main__:main',
            'dedop_gui = dedop.gui.__main__:main',
        ]
    },
    # author_email='',
    # maintainer='',
    # maintainer_email='',
    # url='',
)
