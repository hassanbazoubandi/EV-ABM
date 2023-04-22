YOU:
	echo "make"

lint:
	bash lint.sh .

interface_generate:
	rm -fr model/interface
	stubgen -o model/interface  model

interface_generate2:
	rm -fr model/interface
	stubgen -o model/interface model/Cars.py model/City.py model/Corporations.py model/Customer.py model/Goverment.py model/Society.py
