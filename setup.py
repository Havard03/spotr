"""Setup script for spotrpy package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='spotrpy',
    version='4.1',
    packages=find_packages(),
    python_requires = ">=3.6",
    author = "Havard03",
    author_email = "havard.buvang@gmail.com",
    description = "A simple spotify tool for the terminal",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Havard03/spotr",
    keywords = 'cli',
    install_requires=[
        'Pillow',
        'questionary',
        'requests',
        'rich',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'spotr=spotrpy.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
