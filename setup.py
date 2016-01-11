from setuptools import setup

setup(
    name="toolscake",
    version="0.0.1",
    author="Lorenz Blum",
    maintainer=['Lorenz Blum', 'Witold Wolski'],
    author_email="blum@id.ethz.ch",
    maintainer_email=["blum@id.ethz.ch",'wewolski@gmail.com'],
    description="doing this and that",
    license="BSD",
    packages=['toolscake'],
    url='https://github.com/applicake-tools/applicake',
    install_requires=['Unimod','applicake', 'pyteomics', 'ruffus', 'configobj']
)
