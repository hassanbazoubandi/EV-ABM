
YOU:
	echo "make commands are:\n - "lint" run linters\n - "run" "

lint:
	bash lint.sh . model

run:
	python3 -m model

scrap_om:
	python3 -m otomoto-crawler

generate_figs:
	bash generate_figs.sh 
