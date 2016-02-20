# cs4098F
Repository for CS4098 Group F


1:Install library dependencies for PEOS : 

i)TCL (Ubuntu packages tcl and tcl-dev; see also http://www.activestate.com/activetcl; ).

ii)check (Ubuntu package check; see also http://check.sourceforge.net/). Check is only required to run the unit tests, but the kernel build will fail if check is not present.

iii)expect (Ubuntu package expect; see also http://expect.sourceforge.net/). Required to run the acceptance tests in os/kernel/test/accept_tests.

iv)libxml2 (Ubuntu package libxml2; see also http://www.xmlsoft.org/).

v) sudo apt-get install libreadline-dev byacc flex lib32ncurses5-dev


## 2:Install library dependencies for the app :

git:
```sudo apt-get install git```

```sudo apt-get install python-pip```

```sudo pip install Flask```

```sudo pip install graphviz```

```sudo pip install pydot```

If you run into 'global name 'dot_parser' is not defined' error, then do:```
```pip uninstall pyparsing```
```pip install -Iv https://pypi.python.org/packages/source/p/pyparsing/pyparsing-1.5.7.tar.gz#md5=9be0fcdcc595199c646ab317c1d9a709```
```pip install pydot```

## Installation instructions:

1- git clone the repository ``` https://github.com/CS4098F/cs4098F.git ```

2- cd into cs4098F folder. Run git submodule update --init --recursive

3- ```cd peos``` and execute  ```sudo make```  on terminal where the Makefile is

4- go back just one level```cd ..```and run ```python gui.py``` 

5- go to ```http://127.0.0.1:5000/`` in browser to start app


