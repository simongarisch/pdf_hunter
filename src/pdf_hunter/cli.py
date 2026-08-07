import click
import requests

from .search import download_file, get_pdf_urls


@click.command()
@click.argument("url")
@click.option(
    "-d",
    "--download",
    is_flag=True,
    help="Download the discovered PDF files.",
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
    default=".",
    help="Directory to save downloaded PDFs (defaults to current directory).",
)
def main(url: str, download: bool, output_dir: str) -> None:
    """Search for and download PDF file links from a webpage URL."""
    try:
        urls = get_pdf_urls(url)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching page content: {e}", err=True)
        raise click.Abort()

    if not urls:
        click.echo("No PDF URLs found.")
        return

    if download:
        click.echo(f"Found {len(urls)} PDF(s). Downloading to '{output_dir}'...")
        for pdf_url in urls:
            click.echo(f"Downloading '{pdf_url}'")
            download_file(pdf_url, output_dir)
    else:
        for pdf_url in urls:
            click.echo(pdf_url)
