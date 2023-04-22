YOU:
	echo "make"

lint:
	bash lint.sh .

interface_generate:
	rm -fr model/interface
	stubgen -o model/interface  model
