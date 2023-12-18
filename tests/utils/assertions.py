from typing import Dict

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate


def assert_energy_component(component: Dict, expected: EnergyComponentCreate, expected_type: EnergyComponentType):
    assert component["type"] == expected_type.value
    assert component["name"] == expected.name
    assert component["description"] == expected.description


def assert_excel_file_entry(entry: dict, expected, data_column: str):
    assert entry["id"] == expected.id
    assert entry["dataset"]["id"] == expected.ref_dataset
    assert entry["component"]["name"] == expected.component.name
    assert entry["region"]["name"] == expected.region.name
    if entry["region_to"] is not None or expected.region_to is not None:
        assert entry["region_to"]["name"] == expected.region_to.name
    assert entry[data_column] == expected.__getattribute__(data_column)
