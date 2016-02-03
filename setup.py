from setuptools import setup, find_packages

setup(
    name="searchcake",
    version="0.0.5",
    author="Lorenz Blum",
    maintainer=['Lorenz Blum', 'Witold Wolski'],
    author_email="blum@id.ethz.ch",
    maintainer_email=["blum@id.ethz.ch",'wewolski@gmail.com'],
    description="tpp search workflow with peptideprophet and proteinprophet staring from mzXML files",
    license="BSD",
    packages=find_packages(),
    url='https://github.com/applicake-tools/searchcake',
    install_requires=['Unimod','applicake', 'pyteomics', 'ruffus', 'configobj']
)
