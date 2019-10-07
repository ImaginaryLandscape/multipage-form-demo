# Django Multipage Form Demo

This is a demonstration of a Django form that spans multiple pages.

## System Requirements

Python 3
virtualenv

## Installation

Create and activate a python 3 virtual environment, and `pip install`
from the requirements file:

```bash
(new_virtual_env) $ pip install -r requirements.txt
```

This should install Django (the only requirement).

## Configuration

Run migrations:

```bash
(new_virtual_env) $ ./manage.py migrate
```

## Use

### Front-end

You should now be able to run the project with Django's built-in
`runserver` command on port 8000 (or any available port).

```bash
(new_virtual_env) $ ./manage.py runserver 8000
```

You should then be able to use the app in your browser at
`localhost:8000`.  Fill in form fields with test data and click the
"Continue" button until the form is complete.

### Back-end

You should also be able to log into the admin at
`localhost:8000/admin`.

Use the username "admin" and the password "1234" to log in as a
superuser that was created when migrations were run.  Form submissions
should appear in the admin under the "Job Application" app.
