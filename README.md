# pdf-hunter

Search for and download PDF file links from a webpage.

## Installation

```bash
pip install pdf_hunter
```

## CLI Usage

After installing, the `pdf-hunter` executable is made available in your path.

### 1. List PDF links on a webpage

By default, running `pdf-hunter` with a webpage URL will print all discovered absolute PDF links to standard output:

```bash
pdf-hunter "https://example.com/books-list"
```

Output:
```text
https://example.com/books/guide-to-python.pdf
https://example.com/books/advanced-algorithms.pdf
```

### 2. Download PDFs to current directory

Pass the `-d` (or `--download`) flag to download all discovered PDFs to your current directory:

```bash
pdf-hunter "https://example.com/books-list" -d
```

### 3. Download PDFs to a custom directory

Use the `-o` (or `--output-dir`) option to specify a target directory for the downloaded files:

```bash
pdf-hunter "https://example.com/books-list" -d -o /path/to/downloads
```

---

## Python Library Usage

You can also use `pdf-hunter` programmatically in your Python scripts.

```python
import pdf_hunter

url = "https://github.com/EbookFoundation/free-programming-books/blob/main/books/free-programming-books-langs.md"
```

### Get a list of PDF URLs found on a page

```python
pdf_urls = pdf_hunter.get_pdf_urls(url)
print(pdf_urls[:3])
```
Output:
```python
[
    "https://www.cs.uni.edu/~mccormic/4740/guide-c2ada.pdf",
    "http://www.adapower.com/pdfs/AdaDistilled07-27-2003.pdf",
    "https://www.adacore.com/uploads/books/pdf/Ada_for_the_C_or_Java_Developer-cc.pdf",
]
```

### Download a single PDF file

```python
import os

pdf_url = pdf_urls[0]
file_name = pdf_hunter.get_pdf_name(pdf_url)

# Download to a specific directory
pdf_hunter.download_file(pdf_url, folder_path=os.getcwd())
print(os.path.isfile(file_name))  # True
```

### Download all PDF files from a page

```python
pdf_hunter.download_pdf_files(url, folder_path=os.getcwd())
```
