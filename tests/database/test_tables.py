from sqlalchemy.orm import Session


def check_table_exists(cursor, table_name):
    cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return len(cursor.fetchall()) == 1


def test_table_user(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'user')


def test_table_energy_conversion(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'energy_conversion')


def test_table_energy_conversion_factor(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'energy_conversion_factor')


def test_table_energy_sink(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'energy_sink')


def test_table_energy_source(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'energy_source')


def test_table_energy_storage(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'energy_storage')


def test_table_energy_transmission(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'energy_transmission')


def test_table_capacity(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'capacity')


def test_table_consumption(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'consumption')


def test_table_generation(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'generation')


def test_table_region(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'region')
