from setuptools import setup, find_packages


setup(
    name="pdf_hunter",
    version="0.1.5",
    author="Simon Garisch",
    author_email="gatman946@gmail.com",
    description="Download PDF links from a webpage",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",)),
    install_requires=["requests>=2.22.0", "beautifulsoup4>=4.8.1"],
)
