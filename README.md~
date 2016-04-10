# cs4098F
Repository for CS4098 Group F


1:Install library dependencies for PEOS : 

i)TCL (Ubuntu packages tcl and tcl-dev; see also http://www.activestate.com/activetcl; ).

ii)check (Ubuntu package check; see also http://check.sourceforge.net/). Check is only required to run the unit tests, but the kernel build will fail if check is not present.

iii)expect (Ubuntu package expect; see also http://expect.sourceforge.net/). Required to run the acceptance tests in os/kernel/test/accept_tests.

iv)libxml2 (Ubuntu package libxml2; see also http://www.xmlsoft.org/).

v) ```sudo apt-get install libreadline-dev byacc flex lib32ncurses5-dev```


## 2:Install library dependencies for the app :
```sudo apt-get install graphviz git python-pip libgraphviz-dev pkg-config python-dev python3-tk libffi-dev```

```sudo pip install flask```

```sudo pip install graphviz```

```sudo pip install werkzeug```

```sudo pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/" ```

## 3: Install testing dependencies:

1- Open firefox web browser and go to https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/

2- Download the Selenium IDE from the above link

3- Open Selenium IDE by clicking on the Selenium IDE extension icon on the right of the browser window

4- Open the Test Suite from Selinium IDE by going to File->Open and selecting the path cs4098F/Tests/TextInputTesting.html

5- To run the test suits, select the "Run All" option from the toolbar (A green play button with 3 green filled horizontal bars) 


## Installation instructions:

1- git clone the repository ``` https://github.com/CS4098F/cs4098F.git ```

2- ```cd``` into cs4098F folder. Run ```git submodule update --init --recursive```

3- ```cd peosModified/pml``` and execute  ```make```  on terminal where the Makefile is

4- go back just one level```cd ..```and run ```python gui.py``` 

5- go to ```http://127.0.0.1:5000/`` in browser to start app


## Features Implemented:

File Upload
- User selects a file from local storage which is then copied as a temporary file for later use. 
- Content of the uploaded file is loaded into the textarea.

Syntax Analysis
- Upon attempting to create a graph from the selection, the text value from the Text Area is submitted to pmlcheck for error testing.
- The result is parsed and, in the case of an error, the user is returned to the current screen and notified of the error. 

Resource Flow
- A temporary file is created from the value within the text area and is then passed through traverse, resulting in dot file creation.
- The dot file with annoted resources is then converted and displayed as a PDF to allow the user to zoom or move around the resultant graph. 

Analysis Colored Actions
- A temporary file is created from the value within the text area and is then passed through pmlcheck to generate an analysis file which is then used in conjunction with the pml file, generated dot file, and awk file to designate the colors. 
- The resulting PDF file is then displayed to allow the user to zoom or move around the graph. 

