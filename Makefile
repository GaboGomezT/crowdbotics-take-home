clean:
	autoflake --in-place --remove-unused-variables --imports=pydantic,fastapi,app **/*.py
	isort **/*.py
	black **/*.py

run:
	uvicorn main:app --reload