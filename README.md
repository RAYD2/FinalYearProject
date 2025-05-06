# FinalYearProject

to run this application enter these commands in terminal after nagivating to the downloaded directory

navigate to the FinalYearProject file enter the below commands in terminal:

create and activate a conda enviroment

conda create --name new_env python=3.9
conda activate new_env

pip install -r requirements.txt

then naviage to the main file that has manage.py (api_fyp)

run migrations:

python manage.py migrate

run the server:

python manage.py runserver

then navigate to localhost url: 

http://127.0.0.1:8000/

create a superuser to see admin page:

python manage.py createsuperuser
