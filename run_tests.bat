call "./env/Scripts/activate"
python -m pytest
flake8 pdf_hunter
flake8 tests
pause