import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Reverso_API",
    version="0.0.1.alpha.2",
    license="MIT",
    author="Demian Wolf",
    author_email="demianwolfssd@gmail.com",
    description="Reverso.net API for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/demian-wolf/ReversoAPI",
    keywords=["REVERSO", "REVERSO-CONTEXT", "REVERSO CONTEXT", "CONTEXT", "REVERSO-VOICE", "REVERSO VOICE", "VOICE",
              "REVERSO-API", "API", "WRAPPER", "PYTHON"],
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    extras_require={
        "playing spoken text, not just saving it to file-like objects": ["pygame"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ]
)
