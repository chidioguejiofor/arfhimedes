[![Maintainability](https://api.codeclimate.com/v1/badges/9218364beb3a67c80be8/maintainability)](https://codeclimate.com/github/chidioguejiofor/arfhimedes/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/9218364beb3a67c80be8/test_coverage)](https://codeclimate.com/github/chidioguejiofor/arfhimedes/test_coverage)
# User story app

This is a project built in an interview test


### Setup app
You can setup the app by:
- Cloning  repo with `git clone https://github.com/chidioguejiofor/arfhimedes.git`
- Add environmental variables from .env-sample
- Install pipenv using pypi via `pip install pipenv`
- Start a pipenv shell by running `pipenv shell`
- Upgrade db using `flask db upgrade`

### Start the app using
You can start the app by running `python app.py`

### Documentation
Postman: [![Run in Postman](https://run.pstmn.io/button.svg)](https://documenter.getpostman.com/view/4208573/SzRuZYJ1)

### Linting
You can run lint:
```bash 
yapf -ir $(find . -name '*.py')
```