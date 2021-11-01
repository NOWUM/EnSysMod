from ensysmod.core import security


def test_password_hash_equal():
    password = "my-secure-password"
    hashed_password = security.get_password_hash(password)
    assert security.verify_password(password, hashed_password)


def test_password_hash_non_equal():
    password = "my-secure-password"
    hashed_password = security.get_password_hash(password)
    assert not security.verify_password(password + "1", hashed_password)
