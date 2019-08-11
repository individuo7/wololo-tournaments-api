wololo-tournaments-api
======================

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

*Original cookiecutter documentation:* https://github.com/pydanny/cookiecutter-django/blob/2.2.1/%7B%7Bcookiecutter.project_slug%7D%7D/README.rst


Quick start
-----------

::

  docker-compose -f local.yml build
  docker-compose -f local.yml up
  docker-compose -f local.yml run --rm django python manage.py createsuperuser
  docker-compose -f local.yml run --rm django python manage.py populate_database


Useful addresses
----------------

====================  ========================================
Django admin          http://localhost:8000/admin/
Swager documentation  http://localhost:8000/docs/
OpenAPI definition    http://localhost:8000/docs/swagger.json
MailHog client        http://localhost:8025/
Elasticsearch server  http://localhost:9200/
====================  ========================================
