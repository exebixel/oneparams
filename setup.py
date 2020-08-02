from setuptools import setup

setup(
    name="oneparams",
    packages=["oneparams"],
    entry_points={"console_scripts": ["one = oneparams.one:main"]},
    version="0.1.0",
    description="One System Parametrizer",
    author="exebixel",
    author_email="ezequielnat7@gmail.com",
    url="https://github.com/exebixel/oneparams",
    install_requires=["requests", "xlrd", "urllib3", "json"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
