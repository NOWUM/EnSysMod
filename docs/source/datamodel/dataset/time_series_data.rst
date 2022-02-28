****************
Time series data
****************

For all energy components the capacity or operation rate can be provided as time series for each region.

This data can be provided as excel files for easy access.
An example can be found `here <https://github.com/NOWUM/EnSysMod/tree/main/examples/data/dataset-1>`_.

The following attributes are available for maximum capacities:

.. autopydantic_model:: ensysmod.schemas.CapacityMaxCreate
   :model-show-json: False
   :model-show-config-member: False
   :model-show-config-summary: False
   :model-show-validator-members: False
   :model-show-validator-summary: False
   :model-show-field-summary: False
   :field-list-validators: False
   :inherited-members: BaseModel

The following attributes are available for fix capacities:

.. autopydantic_model:: ensysmod.schemas.CapacityFixCreate
   :model-show-json: False
   :model-show-config-member: False
   :model-show-config-summary: False
   :model-show-validator-members: False
   :model-show-validator-summary: False
   :model-show-field-summary: False
   :field-list-validators: False
   :inherited-members: BaseModel

The following attributes are available for maximum operation rate:

.. autopydantic_model:: ensysmod.schemas.OperationRateMaxCreate
   :model-show-json: False
   :model-show-config-member: False
   :model-show-config-summary: False
   :model-show-validator-members: False
   :model-show-validator-summary: False
   :model-show-field-summary: False
   :field-list-validators: False
   :inherited-members: BaseModel

The following attributes are available for fix operation rate:

.. autopydantic_model:: ensysmod.schemas.OperationRateFixCreate
   :model-show-json: False
   :model-show-config-member: False
   :model-show-config-summary: False
   :model-show-validator-members: False
   :model-show-validator-summary: False
   :model-show-field-summary: False
   :field-list-validators: False
   :inherited-members: BaseModel