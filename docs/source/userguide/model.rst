.. _model:

*****
Model
*****


Introduction
============

After creating a dataset, you can create a energy model based on it.
The energy model allows you to create multiple simulations based on one dataset with different parameters.
Therefore you need to specify model parameters, that overrides the default values provided within the dataset.

.. _newModel:

Create a new Model
==================
To create a new model, the API REST interface ``POST /models/`` is addressed. The following parameters should be
provided:

- `name`: Name of the model

- `description`: Description of the model

- `ref_dataset`: ID of the reference dataset on which the model is based on.

- `model_parameters`: The model parameters, that overrides the default values provided within the dataset.

The endpoint returns the id of the newly created model.

A full documentation of the API is available `as redoc documentation <http://10.13.10.51:9000/redoc>`_.

.. openapi:: ./../generated/openapi.json
   :paths:
      /models/

Get Model information
=====================
To get model information, the API REST interface ``GET /models/`` is addressed.
Requires the model_id. The endpoint returns the corresponding model information.
