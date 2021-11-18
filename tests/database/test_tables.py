from sqlalchemy.orm import Session


def check_table_exists(cursor, table_name):
    cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return len(cursor.fetchall()) == 1


def test_table_user(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'user')


def test_table_consumption(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'consumption')


def test_table_energyconversion(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'energyconversion')


def test_table_energysink(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'energysink')


def test_table_energysource(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'energysource')


def test_table_energystorage(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'energystorage')


def test_table_generation(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'generation')


def test_table_region(db: Session):
    assert check_table_exists(db.bind.raw_connection().cursor(), 'region')
