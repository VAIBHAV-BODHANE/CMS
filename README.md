# Requirements

* Python (3.6, 3.7, 3.8, 3.9)
* Django (2.2, 3.0, 3.1)

We **highly recommend** and only officially support the latest patch release of
each Python and Django series.


## Installation
The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/VAIBHAV-BODHANE/CMS.git
$ cd CMS
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p python3 venv
$ source env/bin/activate
```
Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/cms/`.

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test cms_app
```
