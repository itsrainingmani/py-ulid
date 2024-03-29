import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The contents of the Readme file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="py-ulid",
    version="1.0.4",
    description="Python library that provides an implementation of the ULID Specification",
    long_description=README,
    long_description_content_type='text/markdown',
    author="Manikandan Sundararajan",
    author_email="mani@hey.com",
    license="MIT",
    url="https://github.com/itsrainingmani/py-ulid",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
)

