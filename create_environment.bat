call activate py36
python -m venv env
call "./env/Scripts/activate"
pip install -r requirements-dev.txt

REM CREATE A UNIQUE JUPYTER KERNEL FOR THIS PROJECT
pip install ipykernel
ipython kernel install --user --name=pdf_hunter
