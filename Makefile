
YOU:
	echo "make"

lint:
	bash lint.sh . model

run:
	poetry run python3 -m model

scrap_om:
	python3 -m otomoto-crawler

generate_figs:
	bash generate_figs.sh 
