# pdf_hunter

Search for and download PDF file links from a webpage. 

## Installation

```bash
pip install pdf_hunter
```

## Usage

```python
import pdf_hunter

url = "https://github.com/EbookFoundation/free-programming-books/blob/main/books/free-programming-books-langs.md"
```

```python
pdf_urls = pdf_hunter.get_pdf_urls(url)
pdf_urls[:3]
```
[
 'https://www.cs.uni.edu/~mccormic/4740/guide-c2ada.pdf',
 'http://www.adapower.com/pdfs/AdaDistilled07-27-2003.pdf',
 'https://www.adacore.com/uploads/books/pdf/Ada_for_the_C_or_Java_Developer-cc.pdf'
]

## We can download a single PDF file from a given url

```python
pdf_url = pdf_urls[0]
pdf_url
```

'https://www.cs.uni.edu/~mccormic/4740/guide-c2ada.pdf'

```python
file_name = pdf_hunter.get_pdf_name(pdf_url)
file_name
```

'guide-c2ada.pdf'

```python
import os

os.path.isfile(file_name)
```

False

```python
pdf_hunter.download_file(pdf_url, folder_path=os.getcwd())

os.path.isfile(file_name)
```

True

## Or download all PDF files from the page

```python
pdf_hunter.download_pdf_files(url, folder_path=os.getcwd())
```

***
