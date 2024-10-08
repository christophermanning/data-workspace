NAME=data-workspace

build:
	@docker-compose build airflow
	@docker-compose build dbt
	@docker-compose build jupyter

dbt-build:
	@docker-compose run dbt /bin/bash -c "dbt build"

dbt-test:
	@docker-compose run dbt /bin/bash -c "dbt test"

format:
	@docker-compose run airflow bash -c "black ." || true
	@docker-compose run jupyter bash -c "black ." || true
	@docker-compose run jupyter bash -c "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --clear-output */*.ipynb"
	@docker-compose run dbt /bin/bash -c "sqlfluff format" || true

up:
	@docker-compose up

dev:
	-tmux kill-session -t "${NAME}"
	tmux new-session -s "${NAME}" -d -n vi
	tmux send-keys -t "${NAME}:vi" "vi" Enter
	tmux new-window -t "${NAME}" -n shell "/bin/zsh"
	tmux new-window -t "${NAME}" -n build
	tmux send-keys -t "${NAME}:build" "make up" Enter
	tmux select-window -t "${NAME}:vi"
	tmux attach-session -t "${NAME}"
