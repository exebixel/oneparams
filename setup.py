import os
import shutil

import setuptools

from oneparams.config import VERSION

current_dir = os.getcwd()
dist_dir = f'{current_dir}/dist'
build_dir = f'{current_dir}/build'

if os.path.isdir(dist_dir):
    shutil.rmtree(dist_dir)

if os.path.isdir(build_dir):
    shutil.rmtree(build_dir)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oneparams",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['one = oneparams.one:cli'],
    },
    version=VERSION,
    description="One System Parametrizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="exebixel",
    author_email="ezequielnat7@gmail.com",
    url="https://github.com/exebixel/oneparams",
    install_requires=[
        "requests", "pandas>=1.4.0", "urllib3", "xlrd", "openpyxl",
        "click>=7.0", "alive-progress>=2.4.1"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    zip_safe=False,
)
