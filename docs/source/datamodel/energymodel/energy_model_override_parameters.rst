********************************
Energy model override parameters
********************************
The energy model parameter overrides the default values provided within the dataset.

In order to override a specific parameter, you must provide the following parameters:

- `component`: The name of the energy component.
- `attribute`: The name of the parameter. (like `yearly_limit`)
- `operation`: The operation to perform on the parameter. (like `add`, `multiply`, `set`)
- `value`: The value that is used with the operation.


.. autopydantic_model:: ensysmod.schemas.EnergyModelOverrideCreate
   :inherited-members: BaseModel