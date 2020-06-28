import setuptools


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setuptools.setup(
    name="bassa-kmehant",
    version="1.0.0-alpha.1",
    author="Mehant Kammakomati",
    author_email="kmehant@scorelab.org",
    description="Python Client Library for the Bassa Project",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/scorelab/BassaClient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Apache 2.0 License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
)
