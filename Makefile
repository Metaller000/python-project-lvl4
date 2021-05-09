install:
	poetry install

update:
	poetry update

build:
	poetry build

lint:
	poetry run flake8 task_manager

test:
	coverage run --source='.' manage.py test
	coverage report
	coverage xml

migrate:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate
	
runserver:
	poetry run python manage.py runserver