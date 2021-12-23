*******
Dataset
*******

.. _introduction:

Introduction
============


A dataset has different components. It contains commodities, as which energy source is used in the energy system, and the regions, your energy system is based on.
Furthermore the dataset consists of energy sources and sinks, storages, conversions and transmissions.

With one dataset several modeling runs can be performed.

.. _newDataset:

Create a new dataset
====================
To create a new dataset, the API REST interface POST /datasets/ is addressed. As query-parameter, the id of the to-be-created dataset is needed.


.. _readData:

Read data
=========
There are two ways to collect the data for the dataset.

Zip-Upload 
----------
With the Zip-Upload, we've created a way to enter the data in the database with only one use of a API REST interface.
Once a zip file is created in a certain format and with certain files, it can be used as a parameter in the body via the rest api interface datasets/xxx/upload. The xxx should be replaced by the ID of the dataset to which the data is linked to.

The file contains other files and folder in which the components to the energy system are described.
For the regions and commodities there is for each a .json file in which the different regions and commodities are listed with the respective parameters.
A region has as parameter only a name while a commodity has besides a name also a description and a unit, which specifies the unit for the values for the use of this commodity.                                                   
For each of the sections for energy sources, sinks, storages, conversions and transmissions exists a folder. These folders contain other folders that are used as a listing of the various objects. For example, there are zwo folder in the source folder that contains data for two different energy sources.
A folder that maps an object contains a .json file that contains the parameters for the object, which are the same across all regions. If there are parameters that are different for each region, these parameters are stored in one Excel file each. Each region is mapped as a column and the value (or values as a time series) is stored in the column according to the region.

The parameter that are needed for each object are documented here (TODO Link). All of the parameters can be set, but not all of them have to.

To show the structure of the zip file, we have created an example. This can be found `here <https://github.com/NOWUM/EnSysMod/tree/main/examples/data/dataset-1/>`_.

Upload data per REST API interfaces individually
------------------------------------------------
Another way is to upload the data in small pieces via the individual REST interfaces. A list of the interfaces can be found :ref:`here. <rest_endpoints>`..
