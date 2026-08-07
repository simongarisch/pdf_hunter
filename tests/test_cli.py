from unittest import mock

import requests
from click.testing import CliRunner

from pdf_hunter.cli import main


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Search for and download PDF file links from a webpage URL." in result.output
    assert "-d, --download" in result.output
    assert "-o, --output-dir" in result.output


@mock.patch("pdf_hunter.cli.get_pdf_urls")
def test_cli_list_pdfs(mock_get_pdf_urls):
    mock_get_pdf_urls.return_value = [
        "https://example.com/one.pdf",
        "https://example.com/two.pdf",
    ]
    runner = CliRunner()
    result = runner.invoke(main, ["https://example.com"])
    assert result.exit_code == 0
    assert "https://example.com/one.pdf" in result.output
    assert "https://example.com/two.pdf" in result.output
    mock_get_pdf_urls.assert_called_once_with("https://example.com")


@mock.patch("pdf_hunter.cli.get_pdf_urls")
def test_cli_list_no_pdfs(mock_get_pdf_urls):
    mock_get_pdf_urls.return_value = []
    runner = CliRunner()
    result = runner.invoke(main, ["https://example.com"])
    assert result.exit_code == 0
    assert "No PDF URLs found." in result.output


@mock.patch("pdf_hunter.cli.download_file")
@mock.patch("pdf_hunter.cli.get_pdf_urls")
def test_cli_download_pdfs(mock_get_pdf_urls, mock_download_file):
    mock_get_pdf_urls.return_value = [
        "https://example.com/one.pdf",
        "https://example.com/two.pdf",
    ]
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["https://example.com", "-d", "-o", "."])
        assert result.exit_code == 0
        assert "Found 2 PDF(s). Downloading to '.'..." in result.output
        assert "Downloading 'https://example.com/one.pdf'" in result.output
        assert "Downloading 'https://example.com/two.pdf'" in result.output
        assert mock_download_file.call_count == 2
        mock_download_file.assert_has_calls(
            [
                mock.call("https://example.com/one.pdf", "."),
                mock.call("https://example.com/two.pdf", "."),
            ]
        )


@mock.patch("pdf_hunter.cli.get_pdf_urls")
def test_cli_error(mock_get_pdf_urls):
    mock_get_pdf_urls.side_effect = requests.exceptions.RequestException(
        "Connection error"
    )
    runner = CliRunner()
    result = runner.invoke(main, ["https://example.com"])
    assert result.exit_code != 0
    assert "Error fetching page content: Connection error" in result.output
