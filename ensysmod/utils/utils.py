import os
from pathlib import Path
from tempfile import mkstemp

import pandas as pd


def get_project_root() -> Path:
    return Path(__file__).parents[2].resolve()


def create_temp_file(dir: str | Path | None = None, prefix: str | None = None, suffix: str | None = None) -> Path:
    fd, temp_file_path = mkstemp(dir=dir, prefix=prefix, suffix=suffix)
    os.close(fd)
    return Path(temp_file_path)


def remove_file(file_path: Path) -> None:
    file_path.unlink()


def df_or_s(df: pd.DataFrame) -> pd.DataFrame | pd.Series:
    """Convert a dataframe to a series if it has only one row."""
    return df.squeeze(axis=0) if df.shape[0] == 1 else df
