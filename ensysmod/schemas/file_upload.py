import enum

from ensysmod.schemas.base_schema import ReturnSchema


class FileStatus(enum.Enum):
    OK = "OK"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"


class FileUploadResult(ReturnSchema):
    file: str
    status: FileStatus
    message: str | None = None


class ZipArchiveUploadResult(ReturnSchema):
    status: FileStatus
    file_results: list[FileUploadResult]
