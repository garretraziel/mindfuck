default:
	python -c "import pyfuk"
install:
	cp mindfuck.py mindfuck
	chmod +x mindfuck
	cp mindfuck pyfuk.py pyfuk.pyc /usr/bin
	rm mindfuck
