import os
import pytest
import pdf_hunter
from unittest import mock


TEST_URL = "https://github.com/EbookFoundation/free-programming-books/blob/master/free-programming-books.md"  # noqa: E501


def test_get_pdf_urls():
    pdf_urls = pdf_hunter.get_pdf_urls(TEST_URL)
    assert isinstance(pdf_urls, list)
    assert len(pdf_urls) > 0


def test_validate_pdf_url():
    pdf_hunter.validate_pdf_url("https://test_site/books/somefile.pdf")
    with pytest.raises(TypeError):
        pdf_hunter.validate_pdf_url(42)  # must be string
    with pytest.raises(ValueError):
        pdf_hunter.validate_pdf_url("xxx.txt")  # must end with '.pdf'


def test_get_pdf_name():
    pdf_url = "https://people.gnome.org/~swilmet/glib-gtk-dev-platform.pdf"
    file_name = pdf_hunter.get_pdf_name(pdf_url)
    assert file_name == "glib-gtk-dev-platform.pdf"


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def test_download_file():
    pdf_url = "https://people.gnome.org/~swilmet/glib-gtk-dev-platform.pdf"
    folder_path = os.path.dirname(os.path.abspath(__file__))
    file_name = pdf_hunter.get_pdf_name(pdf_url)
    file_path = os.path.join(folder_path, file_name)
    remove_file(file_path)

    pdf_hunter.download_file(pdf_url, folder_path)
    assert os.path.isfile(file_path)
    remove_file(file_path)


def test_download_file_warning():
    pdf_url = "this_will_404.pdf"
    folder_path = os.path.dirname(os.path.abspath(__file__))
    with pytest.warns(UserWarning):
        pdf_hunter.download_file(pdf_url, folder_path)


def get_pdf_urls_test(*args):
    return [
        "https://people.gnome.org/~swilmet/glib-gtk-dev-platform.pdf",
        "http://safehammad.com/downloads/python-idioms-2014-01-16.pdf",
    ]

@mock.patch("pdf_hunter.get_pdf_urls", side_effect=get_pdf_urls_test)
def test_download_pdf_files(mock_func):
    folder_path = os.path.dirname(os.path.abspath(__file__))

    print(pdf_hunter)
    print(dir(pdf_hunter))
    print(mock_func)
    #1/0
    #return
    def remove_test_pdfs():
        for pdf_url in get_pdf_urls_test():
            file_path = os.path.join(
                folder_path, pdf_hunter.get_pdf_name(pdf_url)
            )
            if os.path.isfile(file_path):
                os.remove(file_path)

    remove_test_pdfs()
    pdf_hunter.download_pdf_files(TEST_URL, folder_path)
    assert os.path.isfile("glib-gtk-dev-platform.pdf")
    assert os.path.isfile("python-idioms-2014-01-16.pdf")
    remove_test_pdfs()
