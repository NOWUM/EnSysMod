import enum

from pydantic import BaseModel


class FileStatus(enum.Enum):
    OK = "OK"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"


class FileUploadResult(BaseModel):
    file: str
    status: FileStatus
    message: str | None = None


class ZipArchiveUploadResult(BaseModel):
    status: FileStatus
    file_results: list[FileUploadResult]

    class Config:
        orm_mode = True
