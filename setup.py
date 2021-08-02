from setuptools import find_packages, setup

setup(
    name='SequenceLibrary',
    packages=find_packages(include=['SequenceLibrary']),
    version='0.1.0',
    description='Sequence Library for use with Gene data from Lab and UT Fusion Gene database',
    author='Ethan Speakman',
    license='GNU',
    install_requires=['numpy', 'pandas'],
    setup_requires=[],

)