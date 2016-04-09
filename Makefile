.PHONY: build test install dependencies

build: dependencies

install:dependencies 
	cd peosModified/pml && make
	cd ..

dependencies:
	sudo apt-get install tcl
	sudo apt-get install tcl-dev
	sudo apt-get install check
	sudo apt-get install expect
	sudo apt-get install libxml2 
	sudo apt-get install libreadline-dev
	sudo apt-get install byacc
	sudo apt-get install flex
	sudo apt-get install lib32ncurses5-dev
	sudo apt-get install graphviz 
	sudo apt-get install git
	sudo apt-get install python-pip
	sudo apt-get install libgraphviz-dev
	sudo apt-get install pkg-config
	sudo apt-get install python-dev
	sudo apt-get install python3-tk
	sudo apt-get install libffi-dev
	sudo pip install flask
	sudo pip install graphviz
	sudo pip install werkzeug 
	


	

