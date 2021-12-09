from typing import Dict

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate


def assert_energy_component(component: Dict, expected: EnergyComponentCreate, expected_type: EnergyComponentType):
    assert component["type"] == expected_type.value
    assert component["name"] == expected.name
    assert component["description"] == expected.description
