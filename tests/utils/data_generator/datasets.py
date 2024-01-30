from pathlib import Path
from zipfile import ZipFile

from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.core.file_upload import process_dataset_zip_archive
from ensysmod.model import Dataset, DatasetPermission
from ensysmod.schemas import DatasetCreate, DatasetPermissionCreate, FileStatus
from ensysmod.utils.utils import get_project_root
from tests.utils.data_generator.users import new_user
from tests.utils.utils import get_current_user_from_header, random_string


def dataset_create_request(
    db: Session,
    user_header: dict[str, str],
    *,
    user_id: int | None = None,
    hours_per_time_step: int = 1,
    number_of_time_steps: int = 8760,
) -> DatasetCreate:
    """
    Generate a dataset create request with the specified user_id, hours_per_time_step and number_of_time_steps.
    If user_id is not specified, the current user is used.
    """
    if user_id is None:
        user_id = get_current_user_from_header(db, user_header).id
    return DatasetCreate(
        name=f"Dataset-{random_string()}",
        description=None,
        hours_per_time_step=hours_per_time_step,
        number_of_time_steps=number_of_time_steps,
        cost_unit="1e9 Euro",
        length_unit="km",
        ref_user=user_id,
    )


def new_dataset(
    db: Session,
    user_header: dict[str, str],
    *,
    user_id: int | None = None,
    hours_per_time_step: int = 1,
    number_of_time_steps: int = 8760,
) -> Dataset:
    """
    Create a dataset with the specified user_id, hours_per_time_step and number_of_time_steps.
    If user_id is not specified, the current user is used.
    """
    create_request = dataset_create_request(
        db=db,
        user_header=user_header,
        user_id=user_id,
        hours_per_time_step=hours_per_time_step,
        number_of_time_steps=number_of_time_steps,
    )
    return crud.dataset.create(db=db, obj_in=create_request)


def dataset_permission_create_request(
    db: Session,
    user_header: dict[str, str],
    *,
    ref_user: int | None = None,
) -> DatasetPermissionCreate:
    """
    Generate a dataset for the current user, then generate a dataset permission create request for the specified ref_user.
    If ref_user is not specified, a new user is created.
    """
    ref_dataset = new_dataset(db, user_header).id
    if ref_user is None:
        ref_user = new_user(db).id
    return DatasetPermissionCreate(
        ref_dataset=ref_dataset,
        ref_user=ref_user,
        allow_usage=True,
        allow_modification=True,
        allow_permission_grant=True,
        allow_permission_revoke=True,
    )


def new_dataset_permission(
    db: Session,
    user_header: dict[str, str],
    *,
    ref_user: int | None = None,
) -> DatasetPermission:
    return crud.dataset_permission.create(db=db, obj_in=dataset_permission_create_request(db, user_header, ref_user=ref_user))


EXAMPLE_DATASETS: list[str] = [
    "1node_Example",
    "Multi-regional_Example",
]


def get_dataset_zip(example_dataset: str) -> Path:
    return Path(get_project_root() / "examples" / "datasets" / f"{example_dataset}.zip")


def get_example_dataset(db: Session, user_header: dict[str, str], *, example_dataset: str) -> Dataset:
    """
    Return example dataset entry in db if it exists, otherwise create and fill it with data from example dataset zip.
    """
    dataset = crud.dataset.get_by_name(db, name=example_dataset)
    if dataset is None:
        create_request = DatasetCreate(
            name=example_dataset,
            description=None,
            hours_per_time_step=1,
            number_of_time_steps=8760,
            cost_unit="1e9 Euro",
            length_unit="km",
            ref_user=get_current_user_from_header(db, user_header).id,
        )
        dataset = crud.dataset.create(db=db, obj_in=create_request)

        with ZipFile(get_dataset_zip(example_dataset), "r") as zip_archive:
            result = process_dataset_zip_archive(zip_archive, dataset.id, db)
            assert result.status == FileStatus.OK

    return dataset
