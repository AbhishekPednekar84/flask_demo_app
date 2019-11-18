# Flask Demo Application 
https://bit.ly/flask-app

[![Build Status](https://travis-ci.org/AbhishekPednekar84/flask_demo_app.svg?branch=master)](https://travis-ci.org/AbhishekPednekar84/flask_demo_app) [![Coverage Status](https://coveralls.io/repos/github/AbhishekPednekar84/flask_demo_app/badge.svg)](https://coveralls.io/github/AbhishekPednekar84/flask_demo_app)

## Steps to run a local setup
1. Clone the repository - `git clone https://github.com/AbhishekPednekar84/flask_demo_app`
2. Create and activate a virtual rnvironment
3. Install dependencies - `pip install -r requirements.txt`
4. Create a .env file (refer to the .env.example file) containing the Flask *SECRET_KEY*, *DATABASE_URL* (formerly *SQLALCHEMY_DATABASE_URI*), *RECAPTCHA_PUBLIC_KEY* and *RECAPTCHA_PRIVATE_KEY* values.
5. To discover and run tests - `python -m unittest discover tests`
6. To evaluate code coverage - `coverage run -m tests.test_app`
7. To run a coverage report - `coverage report -m`
8. To run the application - `python app.py`

**Note**: Remember to omit your virtual environment directory in *.coveragerc* before running `coverage report -m`

## Deployment
The application has been deployed in Heroku. Refer to [this](https://www.codedisciples.in/flask-heroku.html) article on [Code Disciples](https://codedisciples.in) for the complete deployment steps.
