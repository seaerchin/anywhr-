# anywhr-
a simple server prepared for the anywhr coding challenge.

a brief overview of the module is as such: 

1. the constants file stores the constants that will be needed for the project. in this case, there was only the mapping from a hexagon's own border to the neighbour's border

2. the hexagon.py file defines a hexagon together with helper methods.
	a. the hexagon file provides CRUD functions on the hexagon objects. 
	b. there are also private methods defined in the file itself to help with the CRUD functions.

3. next, the server.py file defines a server that provides 4 REST endpoints to perform CRUD operations on the hexagons. there is an additional helper method at /state that returns the current state of the hexagons.

Additional notes: there is a tests.py file along with a postman collection file. both of these define tests for the hexagon operations. the test.py file tests the local methods whereas the postman collection tests the REST endpoints.

set-up:

1. setup a virtual env in your working folder.
	a. utilize this command: python3 -m venv /path/to/new/virtual/environment

2. next, activate your venv 
	a. navigate to the scripts folder and type activate (on windows) 
	b. similarly, just type ./activate or source ./activate on linux 

3. install the requirements using pip install -r requirements.txt (note that you have to be at the root of your working dir) 

4. type in python3 server.py!

personal info 

Languages
	1. python 
	2. go 
	3. java 
	4. c#

Frameworks
	1. flask (python) 
	2. unittests (python)
	3. testing (go) 
	4. http (go) 
	5. .net core (c#) 
	6. tensorflow/keras (python) 

Technology
	1. docker
	2. google cloud 
	3. git 
	4. postman 
