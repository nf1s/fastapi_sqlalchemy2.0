default:
	just --list

setup:
	@poetry install --dev --pre

run:
	@poetry run uvicorn main:app --reload

test:
	@poetry run pytest -s

shell:
	@poetry shell

db-run:
	@docker run \
		--rm   \
		--name  postgres \
		-p 5432:5432 \
		-e POSTGRES_USER=postgres \
		-e POSTGRES_PASSWORD=postgres \
		-e POSTGRES_DB=postgres \
		-d postgres

db-stop:
	@docker stop postgres

db-shell:
	@docker exec -it postgres psql -U postgres
