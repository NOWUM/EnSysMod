************************************
Energy model optimization parameters
************************************
The energy model optimization parameters specify the parameters for the myopic optimization function.

In order to perform a myopic optimization, the following parameter must be given:

- `start_year`: Year of the first optimization.

In addition, at least two of the following parameters must also be specified:

- `end_year`: Year of the last optimization.

- `number_of_steps`: Number of optimization runs excluding the start year.

- `years_per_step`: Number of years represented by one optimization run.

The following parameters are optional, but both must be provided if the CO2 reduction is used:

- `CO2_reference`: CO2 emission reference value to which the reduction should be applied to.

- `CO2_reduction_targets`: CO2 reduction targets for all optimization periods, in percentages. If specified, the length of the list must equal the number of optimization steps, and a sink component named 'CO2 to environment' is required.


.. autopydantic_model:: ensysmod.schemas.EnergyModelOptimizationCreate
   :model-show-json: False
   :model-show-config-member: False
   :model-show-config-summary: False
   :model-show-validator-members: False
   :model-show-validator-summary: False
   :model-show-field-summary: False
   :field-list-validators: False
   :inherited-members: BaseModel
   :member-order: bysource