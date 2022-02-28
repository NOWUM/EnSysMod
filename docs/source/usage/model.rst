******
Modell
******

.. _modell:

Introduction
============

The model represents the basis for modeling with the FINE Framework. One Dataset can be used for multiple modeling runs.
A modeling run outputs cost- and CO2 reduction target values to reach the set goals.

.. _newModel:

Create a new Model
==================
To create a new model, the API REST interface ``POST /models/`` is addressed. The following parameters should be
provided:

- `name`: name of the model

- `yearly_co2_limit`: yearly CO2 limit used for calculations within FINE

- `description`: description of the model

- `ref_dataset`: id of the reference dataset on which the model is based on

The endpoint returns the id of the newly created model.

A full documentation of the API is available `as redoc documentation <http://10.13.10.51:9000/redoc>`_.

.. openapi:: ./../generated/openapi.json
   :paths:
      /models/

Get Model information
=====================
To get model information, the API REST interface ``GET /models/`` is addressed.
Requires the model_id. The endpoint returns the corresponding model information.

Update Model information
========================
To get model information, the API REST interface ``PUT /models/`` is addressed. The following parameters can be
changed:

- `name`: name of the model

- `yearly_co2_limit`: yearly CO2 limit used for calculations within FINE

- `description`: description of the model

The endpoint returns the id of the updated model.

Remove Model
============
To remove a new model, the API REST interface ``DELETE /models/`` is addressed. The following parameter should be
provided:

- `model_id`: id of the model

This will remove the corresponding model from the database.
