install:
	poetry install

update:
	poetry update

build:
	poetry build

lint:
	poetry run flake8 task_manager

test:
	./manage.py test

migrate:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate
	
runserver:
	poetry run python manage.py runserver