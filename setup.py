from setuptools import setup, find_packages


setup(
    name="pdf_hunter",
    version="0.1.0",

    author="Simon Garisch",
    author_email="gatman946 at gmail.com",

    description="Download PDF links from a webpage",
    long_description=open("README.md").read(),

    packages=find_packages(exclude=('tests',)),
    install_requires=[],
)
