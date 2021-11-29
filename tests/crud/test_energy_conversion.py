import pytest
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.schemas import EnergyConversionCreate


@pytest.mark.skip(reason="Not working while reworking the models.")
def test_create_energy_conversion(db: Session):
    create = EnergyConversionCreate(name="test_energy_conversion", description="test_energy_conversion desc")
    energy_conversion = crud.energy_conversion.create(db, obj_in=create)
    assert energy_conversion.name == "test_energy_conversion"
    assert energy_conversion.description == "test_energy_conversion desc"
