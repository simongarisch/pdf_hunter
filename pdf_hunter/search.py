import os
import warnings
import six
from bs4 import BeautifulSoup
import requests

if six.PY2:
    from urllib import urlopen
else:
    from urllib.request import urlopen


def get_pdf_urls(url):
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data, features="html.parser")

    pdf_urls = []
    for link in soup.find_all("a"):
        link_address = link.get("href")
        if link_address.endswith(".pdf"):
            pdf_urls.append(link_address)
    return pdf_urls


def validate_pdf_url(pdf_url):
    if not isinstance(pdf_url, str):
        raise TypeError("Expected a url string.")
    if not pdf_url.endswith(".pdf"):
        raise ValueError("Expected link to a pdf file.")


def get_pdf_name(pdf_url):
    validate_pdf_url(pdf_url)
    return pdf_url.split("/")[-1]


def download_file(pdf_url, folder_path=os.getcwd()):
    validate_pdf_url(pdf_url)
    pdf_name = get_pdf_name(pdf_url)
    pdf_path = os.path.join(folder_path, pdf_name)
    pdf_already_downloaded = os.path.isfile(pdf_path)

    if pdf_already_downloaded:
        return  # pragma: no cover

    try:
        response = urlopen(pdf_url)
        with open(pdf_path, "wb") as target_pdf:
            target_pdf.write(response.read())
    except Exception as e:
        msg = "Unable to download '{}': Error {}".format(pdf_url, str(e))
        warnings.warn(msg)


def download_pdf_files(url, folder_path=os.getcwd()):
    pdf_urls = get_pdf_urls(url)
    for pdf_url in pdf_urls:
        print("downloading '{}'".format(pdf_url))
        download_file(pdf_url, folder_path)
