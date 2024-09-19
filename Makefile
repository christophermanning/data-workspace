NAME=data-workspace

build:
	@docker-compose build dbt

shell:
	@docker-compose run dbt /bin/bash

dbt-build:
	@docker-compose run dbt /bin/bash -c "dbt build"

dbt-test:
	@docker-compose run dbt /bin/bash -c "dbt test"

format:
	@docker-compose run dbt /bin/bash -c "sqlfluff format"

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
