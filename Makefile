install:
	poetry install

update:
	poetry update

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

publish:
	poetry publish --dry-run
		
lint:
	poetry run flake8 task_manager

test:
	poetry run pytest -vs tests

migrate:
	poetry run python manage.py migrate

runserver:
	poetry run python manage.py runserver