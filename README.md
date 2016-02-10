# cs4098F
Repository for CS4098 Group F


1:Install library dependencies for PEOS

i)TCL (Ubuntu packages tcl and tcl-dev; see also http://www.activestate.com/activetcl; ).
ii)check (Ubuntu package check; see also http://check.sourceforge.net/). Check is only required to run the unit tests, but the kernel build will fail if check is not present.
iii)expect (Ubuntu package expect; see also http://expect.sourceforge.net/). Required to run the acceptance tests in os/kernel/test/accept_tests.
iv)libxml2 (Ubuntu package libxml2; see also http://www.xmlsoft.org/).

2:Install library dependencies for the app
git  -- "sudo apt-get install git"
flask -- pip install Flask

Installation instructions
1- git clone the repository
2- execute  sudo make  on terminal where the Makefile is
3- run python gui.py on terminal 
3- go to http://127.0.0.1:5000/ in browser


