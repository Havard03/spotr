"""Setup script for spotrpy package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='spotrpy',
    version='2.1',
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
        'Pillow==10.1.0',
        'questionary==2.0.1',
        'requests==2.28.1',
        'rich==13.6.0',
        'tqdm==4.66.1',
    ],
    entry_points={
        'console_scripts': [
            'spotr=spotrpy.spotr:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
    ],
)