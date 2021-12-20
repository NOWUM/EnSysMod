import enum
from typing import Optional, List

from pydantic import BaseModel


class FileStatus(enum.Enum):
    OK = 'OK'
    ERROR = 'ERROR'
    SKIPPED = 'SKIPPED'


class FileUploadResult(BaseModel):
    file: str
    status: FileStatus
    message: Optional[str] = None


class ZipArchiveUploadResult(BaseModel):
    status: FileStatus
    file_results: List[FileUploadResult]

    class Config:
        orm_mode = True
