**********
Excel data
**********

All components
==============
For all energy components, these data can be provided via the REST API, or as excel files for easy access.
If provided as excel files, the number and the name of the columns must correspond to the regions defined in the dataset. For capacities and full load hours, there should be exactly one row. For operation rates, the number of rows must correspond to the number of time steps defined in the dataset.

Examples can be found `here <https://github.com/NOWUM/EnSysMod/tree/main/examples>`_.

Fix Capacity
------------
The following attributes are available for fix capacities:

.. autopydantic_model:: ensysmod.schemas.CapacityFixCreate
   :inherited-members: BaseModel

Max Capacity
------------
The following attributes are available for maximum capacities:

.. autopydantic_model:: ensysmod.schemas.CapacityMaxCreate
   :inherited-members: BaseModel

Min Capacity
------------
The following attributes are available for minimum capacities:

.. autopydantic_model:: ensysmod.schemas.CapacityMinCreate
   :inherited-members: BaseModel

Fix Operation Rate
------------------
The following attributes are available for fix operation rate:

.. autopydantic_model:: ensysmod.schemas.OperationRateFixCreate
   :inherited-members: BaseModel

Max Operation Rate
------------------
The following attributes are available for maximum operation rate:

.. autopydantic_model:: ensysmod.schemas.OperationRateMaxCreate
   :inherited-members: BaseModel

Max Yearly Full Load Hours
--------------------------
The following attributes are available for maximum yearly full load hours:

.. autopydantic_model:: ensysmod.schemas.YearlyFullLoadHoursMaxCreate
   :inherited-members: BaseModel

Min Yearly Full Load Hours
--------------------------
The following attributes are available for minimum yearly full load hours:

.. autopydantic_model:: ensysmod.schemas.YearlyFullLoadHoursMinCreate
   :inherited-members: BaseModel

Transmission components
=======================
Additionaly, transmission distances and losses can also be provided for transmission components, via REST API or as excel files.
If provided as excel files, the number and the name of rows and columns must correspond to the regions defined in the dataset.

Examples can be found `here <https://github.com/NOWUM/EnSysMod/tree/main/examples>`_.

Transmission Distance
---------------------
The following attributes are available for transmission distances:

.. autopydantic_model:: ensysmod.schemas.TransmissionDistanceCreate
   :inherited-members: BaseModel

Transmission Loss
-----------------
The following attributes are available for transmission losses:

.. autopydantic_model:: ensysmod.schemas.TransmissionLossCreate
   :inherited-members: BaseModel
