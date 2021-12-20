from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.model import EnergyConversion
from ensysmod.schemas import EnergyConversionCreate, EnergyConversionUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyConversion(CRUDBaseDependsComponent[EnergyConversion, EnergyConversionCreate, EnergyConversionUpdate]):
    """
    CRUD operations for EnergyConversion
    """

    def create(self, db: Session, *, obj_in: EnergyConversionCreate) -> EnergyConversion:
        commodity = crud.energy_commodity.get_by_dataset_and_name(db, name=obj_in.commodity_unit,
                                                                  dataset_id=obj_in.ref_dataset)
        obj_in_dict = obj_in.dict()
        obj_in_dict['ref_commodity_unit'] = commodity.id
        db_obj = super().create(db=db, obj_in=obj_in_dict)

        # save energy conversion factors
        for factor_create in obj_in.conversion_factors:
            factor_create.ref_dataset = obj_in.ref_dataset
            factor_create.ref_component = db_obj.component.id
            crud.energy_conversion_factor.create(db, obj_in=factor_create)

        return db_obj


energy_conversion = CRUDEnergyConversion(EnergyConversion)
