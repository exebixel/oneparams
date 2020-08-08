import setuptools

setuptools.setup(
    name="oneparams",
    packages=setuptools.find_packages(),
    # packages=["oneparams"],
    scripts=['bin/one'],
    version="0.1.9",
    description="One System Parametrizer",
    author="exebixel",
    author_email="ezequielnat7@gmail.com",
    url="https://github.com/exebixel/oneparams",
    install_requires=["requests", "xlrd", "urllib3"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux"
    ],
    zip_safe=False,
)
