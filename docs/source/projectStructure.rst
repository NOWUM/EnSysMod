Project structure
=================

This documentation should help developers understanding the project structure.

:: 

    project       
    ├── docs/
    │   └── source/  
    ├── EnSysMod/
    │   ├── api/
    │   ├── core/
    │   ├── crud/
    │   ├── database/
    │   ├── model/
    │   ├── schemas/
    │   ├── main.py
    │   └── app.py 
    ├── scripts/
    ├── tests/
    ├── requirements.txt
    ├── requirements-dev.txt
    ├── setup.cfg
    └── setup.py

    
Repository structure
--------------------
* ``docs/`` contains everything needed for documentation. The subfolder ``source/`` contains ``.rst`` files containing the documentation. A rst-cheatsheet can be found here https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst.
* ``EnSysMod/`` contains the actual python project.
* ``scripts/`` contains multiple scripts to install, test and run the project.
* ``tests/`` contains the pytest tests to test the python project.
* ``requirements.txt`` contains the required python dependencies in order to run the project in production mode.
* ``requirements-dev.txt`` contains addition python dependencies for development.
* ``setup.cfg`` and ``setup.py`` are some stuff needed for correct project setup. 

Python project structure
------------------------
The python project structure is based on the FastAPI postgresql example (https://github.com/tiangolo/full-stack-fastapi-postgresql).

* ``api/`` contains the endpoints of the REST-API. 
* ``core/`` contains multiple core functions of the project.
* ``crud/`` represents the data query and data manipulation layer. It provides functions to query and manipulate the data in the database.
* ``database/`` contains some stuff to get the database running.
* ``model/`` contains the database models. These Models will be converted to tables in the database.
* ``schemas/`` contains some classes that represents the requests and responses of the REST-API.