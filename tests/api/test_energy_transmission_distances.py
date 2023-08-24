from typing import Dict

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import EnergyTransmissionDistanceUpdate
from tests.utils import data_generator
from tests.utils.assertions import assert_transmission_distance
from tests.utils.data_generator.energy_transmissions import create_transmission_scenario
from tests.utils.utils import clear_database


def test_create_transmission_distance(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a transmission distance.
    """
    create_request = data_generator.fixed_transmission_distance_create(db)
    response = client.post("/distances/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_distance = response.json()
    assert created_distance["distance"] == create_request.distance
    assert created_distance["transmission"]["component"]["name"] == create_request.component
    assert created_distance["region_from"]["name"] == create_request.region_from
    assert created_distance["region_to"]["name"] == create_request.region_to


def test_create_existing_transmission_distance(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating an existing transmission distance.
    """
    clear_database(db)
    create_request = data_generator.fixed_transmission_distance_create(db)
    response = client.post("/distances/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/distances/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_transmission_distance_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a transmission distance with unknown dataset.
    """
    create_request = data_generator.fixed_transmission_distance_create(db)
    create_request.ref_dataset = 123456
    response = client.post("/distances/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_transmission_distance_unknown_component(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a transmission distance with unknown component.
    """
    create_request = data_generator.fixed_transmission_distance_create(db)
    create_request.component = "Unknown Component"
    response = client.post("/distances/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_transmission_distance_unknown_regions(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a transmission distance with unknown regions.
    """
    create_request = data_generator.fixed_transmission_distance_create(db)
    create_request.region_from = "Unknown Region"
    response = client.post("/distances/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    create_request = data_generator.fixed_transmission_distance_create(db)
    create_request.region_to = "Unknown Region"
    response = client.post("/distances/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_all_transmission_distances(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all transmission distances.
    """
    clear_database(db)
    scenario = create_transmission_scenario(db)

    response = client.get("/distances/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    distance_list = response.json()
    assert len(distance_list) == 4
    assert_transmission_distance(check_entry=distance_list[0], expected_entry=scenario["distances"][0])
    assert_transmission_distance(check_entry=distance_list[1], expected_entry=scenario["distances"][1])
    assert_transmission_distance(check_entry=distance_list[2], expected_entry=scenario["distances"][2])
    assert_transmission_distance(check_entry=distance_list[3], expected_entry=scenario["distances"][3])


def test_get_transmission_distance(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving a transmission distance.
    """
    existing_distance = data_generator.fixed_existing_transmission_distance(db)
    response = client.get(f"/distances/{existing_distance.id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    retrieved_distance = response.json()
    assert_transmission_distance(check_entry=retrieved_distance, expected_entry=existing_distance)


def test_get_transmission_distances_by_component(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test retrieving all transmission distances of a component.
    """
    clear_database(db)
    scenario = create_transmission_scenario(db)

    component_id = scenario["transmissions"][0].component.id
    response = client.get(f"/distances/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    distance_list = response.json()
    assert len(distance_list) == 2
    assert_transmission_distance(check_entry=distance_list[0], expected_entry=scenario["distances"][0])
    assert_transmission_distance(check_entry=distance_list[1], expected_entry=scenario["distances"][1])

    component_id = scenario["transmissions"][1].component.id
    response = client.get(f"/distances/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    distance_list = response.json()
    assert len(distance_list) == 2
    assert_transmission_distance(check_entry=distance_list[0], expected_entry=scenario["distances"][2])
    assert_transmission_distance(check_entry=distance_list[1], expected_entry=scenario["distances"][3])


def test_update_transmission_distance(db: Session, client: TestClient, normal_user_headers: Dict[str, str]):
    """
    Test updating a transmission distance.
    """
    existing_distance = data_generator.fixed_existing_transmission_distance(db)
    print(existing_distance.distance)

    update_request = EnergyTransmissionDistanceUpdate(**jsonable_encoder(existing_distance))
    update_request.distance = 1234

    response = client.put(
        f"/distances/{existing_distance.id}",
        headers=normal_user_headers,
        data=update_request.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    updated_distance = response.json()
    assert updated_distance["distance"] == update_request.distance


def test_remove_transmission_distance(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test deleting a transmission distance.
    """
    clear_database(db)
    scenario = create_transmission_scenario(db)

    # delete the first distance entry
    response = client.delete(f"/distances/{scenario['distances'][0].id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    # check that the database only has the remaining distance entries
    get_response = client.get("/distances/", headers=normal_user_headers)
    assert get_response.status_code == status.HTTP_200_OK

    distance_list = get_response.json()
    assert len(distance_list) == 3
    assert_transmission_distance(check_entry=distance_list[0], expected_entry=scenario["distances"][1])
    assert_transmission_distance(check_entry=distance_list[1], expected_entry=scenario["distances"][2])
    assert_transmission_distance(check_entry=distance_list[2], expected_entry=scenario["distances"][3])


def test_remove_transmission_distances_by_component(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test deleting all transmission distances of a component.
    """
    clear_database(db)
    scenario = create_transmission_scenario(db)

    # delete the distance entries of the first component
    component_id = scenario["transmissions"][0].component.id
    response = client.delete(f"/distances/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    # check that the database only has distance entries from the second component
    get_response = client.get("/distances/", headers=normal_user_headers)
    assert get_response.status_code == status.HTTP_200_OK

    distance_list = get_response.json()
    assert len(distance_list) == 2
    assert_transmission_distance(check_entry=distance_list[0], expected_entry=scenario["distances"][2])
    assert_transmission_distance(check_entry=distance_list[1], expected_entry=scenario["distances"][3])
