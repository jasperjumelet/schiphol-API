# Schiphol API
This is an API for Schiphol were you can get different data from Schiphol


## Run Locally  

Clone the project  

~~~bash  
  git clone https://github.com/jasperjumelet/impalatest.git
~~~

Go to the project directory  

~~~bash  
  cd impalatest
~~~


To install all the dependencies and start the server run

~~~bash  
docker-compose up 
~~~

or if you prefer to run without docker
~~~bash
pip install requirements.txt
python run.py
~~~

## Tests 

Tests can be run 2 different ways.

1. make sure you have requirements installed then locally run
~~~bash
pytest
~~~ 

2. from within a docker container
~~~bash
docker-compose run test
~~~

## Architecture
![Architecture](images/impala_diagram.drawio.png)