# Subida Cartera!

Proyecto de EDA6 - Legendary Wallabies

## Packages installed:
To be completed soon.

## To install the dependencies:
pip install pipenv --> Install pipenv\
pipenv install --> Install dependencies. Also, this command also creates and activates a virtual env with the dependencies intalled.\
exit --> exit the virtual env\
pipenv shell --> activate the virtual env\

## To run program:
python3 src/subida.py\

## To run the containerized program, with Docker:
1- Remember to start your Docker engine!

2- Build image with:\
docker build -t subida_cartera .\

3- Then, run image with:\
docker run -it subida_cartera

## To run tests:

pytest tests/ --> run all existing tests\
pytest tests/some_test.py --> run the specif file with all the test that has inside\
pytest test/some_test.py -k test_foo run the specif test in this file\
pytest tests/some_test.py -vv  --> verbose\
pytest tests/some_test.py -s --> to debug using ipbd\

## To start the Dash app in a browser:
1- In your console, you mus go to the folder web_app\
2- Type **python3 main.py**. This should open a web page in localhost. The console will tell the address.
3- If oyu want to run the debug mode (that allows the use of ipdb), got yo file **web_app/main.py** and find the line:
```
DEBUG = bool(int(os.getenv("DEBUG", "0")))
````
In this line, replace the "0" parameter with "1".

## If you get a ModuleNotFoundError: No module named 'src:
In this case, I recommend using pyenv and set the environment variable PYTHONPATH to your project folder by typing:\

on mac:\
export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"

on windows:\
set PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"

