# Requirements

* Python (3.6, 3.7, 3.8, 3.9)
* Django (2.2, 3.0, 3.1)

We **highly recommend** and only officially support the latest patch release of
each Python and Django series.


## Installation
Setup project environment with [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io).

```bash
$ virtualenv venv
$ source venv/bin/activate or venv\Scripts\activate (For Windows)
$ pip install -r equirements.txt
$ python manage.py migrate
$ python manage.py runserver
