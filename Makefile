
YOU:
	echo "make"

lint:
	bash lint.sh .

run:
	poetry run python3 -m model

scrap_om:
	python3 -m otomoto-crawler
	