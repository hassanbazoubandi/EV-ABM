
YOU:
	echo "make commands are:\n - \"lint\" run linters\n - \"run\" run example trajectory\n - \"scrap_om\" initial otomoto crowler to downloada actual data\n - \"generate_figs\" run model with different parameters and save results to \"pictures\" folder"

lint:
	bash lint.sh . model

run:
	python3 -m model

scrap_om:
	python3 -m otomoto-crawler

generate_figs:
	bash generate_figs.sh 
