# cs4098F
Repository for CS4098 Group F


1:Install library dependencies for PEOS : 

i)TCL (Ubuntu packages tcl and tcl-dev; see also http://www.activestate.com/activetcl; ).

ii)check (Ubuntu package check; see also http://check.sourceforge.net/). Check is only required to run the unit tests, but the kernel build will fail if check is not present.

iii)expect (Ubuntu package expect; see also http://expect.sourceforge.net/). Required to run the acceptance tests in os/kernel/test/accept_tests.

iv)libxml2 (Ubuntu package libxml2; see also http://www.xmlsoft.org/).

v) ```sudo apt-get install libreadline-dev byacc flex lib32ncurses5-dev```


## 2:Install library dependencies for the app :
```sudo apt-get install graphviz git python-pip libgraphviz-dev pkg-config python-dev python3-tk```

```sudo pip install flask```

```sudo pip install graphviz```

```sudo pip install werkzeug```

```sudo pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/" ```


## Installation instructions:

1- git clone the repository ``` https://github.com/CS4098F/cs4098F.git ```

2- ```cd``` into cs4098F folder. Run ```git submodule update --init --recursive```

3- ```cd peos``` and execute  ```make```  on terminal where the Makefile is

4- go back just one level```cd ..```and run ```python gui.py``` 

5- go to ```http://127.0.0.1:5000/`` in browser to start app


Features Implemented:

File Upload

Syntax Analysis

Resource Flow


Features in Testing:

Analysis Colored Actions


Features in Production:

Social Network

Agent Colored Actions 
