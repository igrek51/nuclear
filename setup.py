import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
    name="cliglue",
    version="0.2.3",
    author="igrek51",
    author_email="igrek51.dev@gmail.com",
    description="Declarative parser for command line interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/igrek51/cliglue",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    license='MIT',
    python_requires='>=3.6.0',
)
