*******
Dataset
*******

This class is the main class of the dataset. It contains general information about the dataset.

Follow :ref:`this <newDataset>` guide to create a new dataset and learn how to provide the data of an energy
system model.

The following attributes are available:

.. autopydantic_model:: ensysmod.schemas.DatasetCreate
   :model-show-json: False
   :model-show-config-member: False
   :model-show-config-summary: False
   :model-show-validator-members: False
   :model-show-validator-summary: False
   :model-show-field-summary: False
   :field-list-validators: False
   :inherited-members: BaseModel


.. _dataset_permissions:

Dataset permissions
===================

After creating a dataset, you can set permissions for the dataset.
You can grant (or revoke) permissions to other users to access and modify the dataset.
By default only you can access and modify the dataset.


The following attributes are available:

.. autopydantic_model:: ensysmod.schemas.DatasetPermissionCreate
   :model-show-json: False
   :model-show-config-member: False
   :model-show-config-summary: False
   :model-show-validator-members: False
   :model-show-validator-summary: False
   :model-show-field-summary: False
   :field-list-validators: False
   :inherited-members: BaseModel


You can modify the permissions for the dataset by using the REST API:

.. openapi:: ./../../generated/openapi.json
   :paths:
      /datasets/permissions/