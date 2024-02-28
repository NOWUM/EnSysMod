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
    *,
    name: str | None = None,
    hours_per_time_step: int = 1,
    number_of_time_steps: int = 8760,
) -> DatasetCreate:
    """
    Generate a dataset create request with the specified name, hours_per_time_step and number_of_time_steps.
    """
    return DatasetCreate(
        name=name if name is not None else f"Dataset-{random_string()}",
        description=None,
        hours_per_time_step=hours_per_time_step,
        number_of_time_steps=number_of_time_steps,
        cost_unit="1e9 Euro",
        length_unit="km",
    )


def new_dataset(
    db: Session,
    user_header: dict[str, str],
    *,
    ref_user: int | None = None,
    name: str | None = None,
    hours_per_time_step: int = 1,
    number_of_time_steps: int = 8760,
) -> Dataset:
    """
    Create a dataset with the specified ref_user, hours_per_time_step and number_of_time_steps.
    If ref_user is not specified, the current user is used.
    """
    create_request = dataset_create_request(
        name=name,
        hours_per_time_step=hours_per_time_step,
        number_of_time_steps=number_of_time_steps,
    )
    create_request_dict = create_request.model_dump()
    create_request_dict["ref_user"] = ref_user if ref_user is not None else get_current_user_from_header(db, user_header).id
    return crud.dataset.create(db=db, obj_in=create_request_dict)


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
        dataset = new_dataset(
            db,
            user_header,
            name=example_dataset,
            hours_per_time_step=1,
            number_of_time_steps=8760,
        )

        with ZipFile(get_dataset_zip(example_dataset), "r") as zip_archive:
            result = process_dataset_zip_archive(zip_archive, dataset.id, db)
            assert result.status == FileStatus.OK

    return dataset
