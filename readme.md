# Subida Cartera!

Proyecto de EDA6 - Legendary Wallabies

Packages installed:
completar acá

## To install the dependencies:
pip install pipenv --> Install pipenv
pipenv install --> Install dependencies. Also, this command also creates and activates an virtual env with the dependencies intalled.
exit --> exit the virtual env
pipenv shell --> activate the virtual env

## To run tests

pytest tests/ --> run all existing tests
pytest tests/some_test.py --> run the specif file with all the test that has inside
pytest test/some_test.py -k test_foo run the specif test in this file
pytest tests/some_test.py -vv  --> verbose
pytest tests/some_test.py -s --> to debug using ipbd

## If you get a ModuleNotFoundError: No module named 'src:
In this case, I recommend using pyenv and set the environment variable PYTHONPATH to your project folder by typing:
on mac:
export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"
on windows:
set PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"

