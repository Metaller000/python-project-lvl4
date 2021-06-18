install:
	poetry install

update:
	poetry update

build:
	poetry build

lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

migrate:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate
	
runserver:
	poetry run python manage.py runserver

lang_compale:
	poetry run django-admin compilemessages
	
run: message_update lang_compale migrate runserver

message_update:
	poetry run python3 manage.py makemessages --all

shell:
	poetry run python3 manage.py shell