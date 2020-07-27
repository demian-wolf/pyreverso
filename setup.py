import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Reverso_API",
    version="0.0.1.beta.2",
    license="MIT",
    author="Demian Wolf",
    author_email="demianwolfssd@gmail.com",
    description="Reverso.net API for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/demian-wolf/ReversoAPI",
    download_url="https://github.com/demian-wolf/ReversoAPI/archive/v.0.0.1.beta.2.tar.gz",
    keywords=["REVERSO", "REVERSO-CONTEXT", "REVERSO CONTEXT", "CONTEXT", "REVERSO-VOICE", "REVERSO VOICE", "VOICE",
              "REVERSO-API", "API", "WRAPPER", "PYTHON"],
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml",
    ],
    extras_require={
        "playing spoken text instead of just getting its MP3 data and/or saving it to file-like objects": ["pygame"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ]
)
