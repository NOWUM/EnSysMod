**********************
Energy model parameter
**********************
The energy model parameter overrides the default values provided within the dataset.

In order to override a specific parameter, you must provide the following parameters:
- `component`: The name of the energy component.
- `attribute`: The name of the parameter. (like `yearly_limit`)
- `operation`: The operation to perform on the parameter. (like `add`, `multiply`, `set`)
- `value`: The value that is used with the operation.


.. autopydantic_model:: ensysmod.schemas.EnergyModelParameterCreate
   :model-show-json: False
   :model-show-config-member: False
   :model-show-config-summary: False
   :model-show-validator-members: False
   :model-show-validator-summary: False
   :model-show-field-summary: False
   :field-list-validators: False
   :inherited-members: BaseModel