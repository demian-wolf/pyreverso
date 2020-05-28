import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Reverso_API",
    version="0.0.1",
    author="Demian Volkov aka Demian Wolf",
    author_email="demianwolfssd@gmail.com",
    description="Reverso.net API for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/demian-wolf/ReversoAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)