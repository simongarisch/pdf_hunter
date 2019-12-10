
# pdf_hunter

Search for and download PDF file links from a webpage. 

## Installation

This has been tested using Python 3 and Python 2.7.

```
pip install pdf_hunter
```

## Usage


```python
import pdf_hunter

url = "https://github.com/EbookFoundation/free-programming-books/blob/master/free-programming-books.md"
```


```python
pdf_urls = pdf_hunter.get_pdf_urls(url)
pdf_urls[:10]
```




    ['https://people.gnome.org/~swilmet/glib-gtk-dev-platform.pdf',
     'https://www.math.upenn.edu/~wilf/AlgoComp.pdf',
     'http://cslibrary.stanford.edu/110/BinaryTrees.pdf',
     'http://www-inst.eecs.berkeley.edu/~cs61b/fa14/book2/data-structures.pdf',
     'http://lib.mdp.ac.id/ebook/Karya%20Umum/Dsa.pdf',
     'http://cslibrary.stanford.edu/103/LinkedListBasics.pdf',
     'http://cslibrary.stanford.edu/105/LinkedListProblems.pdf',
     'http://www.jjj.de/fxt/fxtbook.pdf',
     'http://www.cs.cmu.edu/~rwh/theses/okasaki.pdf',
     'http://igm.univ-mlv.fr/~mac/REC/text-algorithms.pdf']



## We can download a single PDF file from a given url


```python
pdf_url = pdf_urls[0]
pdf_url
```




    'https://people.gnome.org/~swilmet/glib-gtk-dev-platform.pdf'




```python
file_name = pdf_hunter.get_pdf_name(pdf_url)
file_name
```




    'glib-gtk-dev-platform.pdf'




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
