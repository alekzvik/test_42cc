app=contact requests_log models_log

run:
	python manage.py runserver

syncdb:
	python manage.py syncdb --noinput

test:
	python manage.py test ${app}

func_tests:
	python manage.py test functional_tests
