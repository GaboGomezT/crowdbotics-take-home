clean:
	autoflake --in-place --remove-unused-variables --imports=pydantic,fastapi **/**/*.py
	isort **/**/*.py
	black **/**/*.py

run:
	uvicorn app.main:app --reload