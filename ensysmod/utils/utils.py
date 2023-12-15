import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import mkstemp


def create_temp_file(dir: str | Path | None = None, prefix: str | None = None, suffix: str | None = None) -> Path:
    fd, temp_file_path = mkstemp(dir=dir, prefix=prefix, suffix=suffix)
    os.close(fd)
    return Path(temp_file_path)

def remove_file(file_path: Path) -> None:
    file_path.unlink()

@contextmanager
def chdir(path: Path | str):
    # In Python 3.11 use contextlib.chdir().
    current_dir = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(current_dir)
