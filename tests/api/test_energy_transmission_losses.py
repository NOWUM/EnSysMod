from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import EnergyTransmissionLossUpdate
from tests.utils.assertions import assert_transmission_loss
from tests.utils.data_generator.energy_transmissions import (
    create_transmission_scenario,
    transmission_loss_create,
    transmission_loss_create_request,
)
from tests.utils.utils import clear_database


def test_create_transmission_loss(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a transmission loss.
    """
    create_request = transmission_loss_create_request(db, normal_user_headers)
    response = client.post("/losses/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_loss = response.json()
    assert created_loss["loss"] == create_request.loss
    assert created_loss["transmission"]["component"]["name"] == create_request.component
    assert created_loss["region_from"]["name"] == create_request.region_from
    assert created_loss["region_to"]["name"] == create_request.region_to


def test_create_existing_transmission_loss(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating an existing transmission loss.
    """
    clear_database(db)
    create_request = transmission_loss_create_request(db, normal_user_headers)
    response = client.post("/losses/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/losses/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_transmission_loss_unknown_dataset(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a transmission loss with unknown dataset.
    """
    create_request = transmission_loss_create_request(db, normal_user_headers)
    create_request.ref_dataset = 123456
    response = client.post("/losses/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_transmission_loss_unknown_component(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a transmission loss with unknown component.
    """
    create_request = transmission_loss_create_request(db, normal_user_headers)
    create_request.component = "Unknown Component"
    response = client.post("/losses/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_transmission_loss_unknown_regions(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test creating a transmission loss with unknown regions.
    """
    create_request = transmission_loss_create_request(db, normal_user_headers)
    create_request.region_from = "Unknown Region"
    response = client.post("/losses/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    create_request = transmission_loss_create_request(db, normal_user_headers)
    create_request.region_to = "Unknown Region"
    response = client.post("/losses/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_all_transmission_losses(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test retrieving all transmission losses.
    """
    clear_database(db)
    scenario = create_transmission_scenario(db, normal_user_headers)

    response = client.get("/losses/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    loss_list = response.json()
    assert len(loss_list) == 4
    assert_transmission_loss(check_entry=loss_list[0], expected_entry=scenario["losses"][0])
    assert_transmission_loss(check_entry=loss_list[1], expected_entry=scenario["losses"][1])
    assert_transmission_loss(check_entry=loss_list[2], expected_entry=scenario["losses"][2])
    assert_transmission_loss(check_entry=loss_list[3], expected_entry=scenario["losses"][3])


def test_get_transmission_loss(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test retrieving a transmission loss.
    """
    existing_loss = transmission_loss_create(db, normal_user_headers)
    response = client.get(f"/losses/{existing_loss.id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    retrieved_loss = response.json()
    assert_transmission_loss(check_entry=retrieved_loss, expected_entry=existing_loss)


def test_get_transmission_losses_by_component(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test retrieving all transmission losses of a component.
    """
    clear_database(db)
    scenario = create_transmission_scenario(db, normal_user_headers)

    component_id = scenario["transmissions"][0].component.id
    response = client.get(f"/losses/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    loss_list = response.json()
    assert len(loss_list) == 2
    assert_transmission_loss(check_entry=loss_list[0], expected_entry=scenario["losses"][0])
    assert_transmission_loss(check_entry=loss_list[1], expected_entry=scenario["losses"][1])

    component_id = scenario["transmissions"][1].component.id
    response = client.get(f"/losses/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    loss_list = response.json()
    assert len(loss_list) == 2
    assert_transmission_loss(check_entry=loss_list[0], expected_entry=scenario["losses"][2])
    assert_transmission_loss(check_entry=loss_list[1], expected_entry=scenario["losses"][3])


def test_update_transmission_loss(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test updating a transmission loss.
    """
    existing_loss = transmission_loss_create(db, normal_user_headers)
    print(existing_loss.loss)

    update_request = EnergyTransmissionLossUpdate(**jsonable_encoder(existing_loss))
    update_request.loss = 0.0001234

    response = client.put(
        f"/losses/{existing_loss.id}",
        headers=normal_user_headers,
        data=update_request.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    updated_loss = response.json()
    assert updated_loss["loss"] == update_request.loss


def test_remove_transmission_loss(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test deleting a transmission loss.
    """
    clear_database(db)
    scenario = create_transmission_scenario(db, normal_user_headers)

    # delete the first distance entry
    response = client.delete(f"/losses/{scenario['distances'][0].id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    # check that the database only has the remaining distance entries
    get_response = client.get("/losses/", headers=normal_user_headers)
    assert get_response.status_code == status.HTTP_200_OK

    loss_list = get_response.json()
    assert len(loss_list) == 3
    assert_transmission_loss(check_entry=loss_list[0], expected_entry=scenario["losses"][1])
    assert_transmission_loss(check_entry=loss_list[1], expected_entry=scenario["losses"][2])
    assert_transmission_loss(check_entry=loss_list[2], expected_entry=scenario["losses"][3])


def test_remove_transmission_losses_by_component(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test deleting all transmission losses of a component.
    """
    clear_database(db)
    scenario = create_transmission_scenario(db, normal_user_headers)

    # delete the distance entries of the first component
    component_id = scenario["transmissions"][0].component.id
    response = client.delete(f"/losses/component/{component_id}", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    # check that the database only has distance entries from the second component
    get_response = client.get("/losses/", headers=normal_user_headers)
    assert get_response.status_code == status.HTTP_200_OK

    loss_list = get_response.json()
    assert len(loss_list) == 2
    assert_transmission_loss(check_entry=loss_list[0], expected_entry=scenario["losses"][2])
    assert_transmission_loss(check_entry=loss_list[1], expected_entry=scenario["losses"][3])
