import os
import warnings
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

from .url_transforms import UrlTransforms


def get_pdf_urls(url: str) -> list[str]:
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data, features="html.parser")

    pdf_urls = []
    for link in soup.find_all("a"):
        link_address = link.get("href")
        if link_address is None:
            continue
        if link_address.endswith(".pdf"):
            pdf_urls.append(urljoin(url, link_address))
    return pdf_urls


def validate_pdf_url(pdf_url: str) -> None:
    if not isinstance(pdf_url, str):
        raise TypeError("Expected a url string.")
    if not pdf_url.endswith(".pdf"):
        raise ValueError("Expected link to a pdf file.")


def get_pdf_name(pdf_url: str) -> str:
    validate_pdf_url(pdf_url)
    return pdf_url.split("/")[-1]


def download_file(pdf_url: str, folder_path: str | None = None) -> None:
    if folder_path is None:
        folder_path = os.getcwd()
    validate_pdf_url(pdf_url)
    pdf_url = UrlTransforms.apply(pdf_url)
    pdf_name = get_pdf_name(pdf_url)
    pdf_path = os.path.join(folder_path, pdf_name)
    pdf_already_downloaded = os.path.isfile(pdf_path)

    if pdf_already_downloaded:
        return  # pragma: no cover

    try:
        response = urlopen(pdf_url)
        with open(pdf_path, "wb") as target_pdf:
            target_pdf.write(response.read())
    except (URLError, HTTPError, OSError, ValueError) as e:
        msg = f"Unable to download '{pdf_url}': Error {e!s}"
        warnings.warn(msg)


def download_pdf_files(url: str, folder_path: str | None = None) -> None:
    if folder_path is None:
        folder_path = os.getcwd()
    pdf_urls = get_pdf_urls(url)
    for pdf_url in pdf_urls:
        print(f"downloading '{pdf_url}'")
        download_file(pdf_url, folder_path)
