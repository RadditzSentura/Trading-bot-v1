# setup.py

from setuptools import setup, find_packages
import os

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='grid_trading_bot',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A robust grid trading bot with logging and error handling.',
    long_description=read('README.md'),  # Ensure you have a README.md
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/grid_trading_bot',  # Replace with your repo
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,  # Includes files from MANIFEST.in
    install_requires=[
        'ccxt',
        'PyYAML',
        'numpy',
        'pandas',
        'ta',  # Technical Analysis library
        'pytest',
        'python-dotenv',
        'sentry-sdk',
    ],
    entry_points={
        'console_scripts': [
            'grid-trading-bot=main:main',  # Points to main() in src/main.py
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    # Optional: specify package data if needed
    # package_data={
    #     '': ['config/*.yml'],  # Example to include YAML files
    # },
    # Optional: include data files
    # data_files=[('config', ['config/config.yml', 'config/credentials.yml'])],
)