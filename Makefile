NAME=data-workspace

.PHONY: goat duckdb

build:
	@docker-compose build airflow
	@docker-compose build dbt
	@docker-compose build duckdb
	@docker-compose build jupyter
	@docker-compose build observable-framework

duckdb:
	@docker-compose run duckdb /bin/bash -c "duckdb dev.duckdb"

dbt-build:
	@docker-compose run dbt /bin/bash -c "dbt build"

dbt-test:
	@docker-compose run dbt /bin/bash -c "dbt test"

observable-clear-cache:
	rm -R observable-framework/src/.observablehq/cache

observable-build:
	docker-compose run observable-framework /bin/bash -c "npm run build"

format:
	@docker-compose run airflow bash -c "black ." || true
	@docker-compose run jupyter bash -c "black ." || true
	@docker-compose run jupyter bash -c "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --clear-output */*.ipynb"
	@docker-compose run dbt /bin/bash -c "sqlfluff format" || true

up:
	@docker-compose up

goat:
	docker build -t goat goat/ && \
	docker run --volume ./goat/:/src --rm -it goat goat -i architecture.txt -o architecture.svg -sds "#2F81F7" -sls "#2F81F7"

dev:
	-tmux kill-session -t "${NAME}"
	tmux new-session -s "${NAME}" -d -n vi
	tmux send-keys -t "${NAME}:vi" "vi" Enter
	tmux new-window -t "${NAME}" -n shell "/bin/zsh"
	tmux new-window -t "${NAME}" -n build
	tmux send-keys -t "${NAME}:build" "make up" Enter
	tmux select-window -t "${NAME}:vi"
	tmux attach-session -t "${NAME}"
