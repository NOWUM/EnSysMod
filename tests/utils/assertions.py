from typing import Dict

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate


def assert_energy_component(component: Dict, expected: EnergyComponentCreate, expected_type: EnergyComponentType):
    assert component["type"] == expected_type.value
    assert component["name"] == expected.name
    assert component["description"] == expected.description


def assert_transmission_distance(check_entry, expected_entry):
    assert check_entry["id"] == expected_entry.id
    assert check_entry["distance"] == expected_entry.distance
    assert check_entry["transmission"]["component"]["id"] == expected_entry.ref_component
    assert check_entry["region"]["id"] == expected_entry.ref_region
    assert check_entry["region_to"]["id"] == expected_entry.ref_region_to


def assert_transmission_loss(check_entry, expected_entry):
    assert check_entry["id"] == expected_entry.id
    assert check_entry["loss"] == expected_entry.loss
    assert check_entry["transmission"]["component"]["id"] == expected_entry.ref_component
    assert check_entry["region"]["id"] == expected_entry.ref_region
    assert check_entry["region_to"]["id"] == expected_entry.ref_region_to
