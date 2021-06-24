migrate:
	@bash scripts/migrate.sh

up:
	@bash scripts/migrate.sh
	@bash scripts/start.sh

test:
	@bash scripts/migrate.sh
	@bash scripts/test.sh

pull_data:
	@bash scripts/set_up_data.sh