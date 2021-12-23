def validate_name(name: str) -> str:
    """
    Validates the name of an object.

    :param name: The name of the object.
    :return: The validated name.
    """
    if not name:
        raise ValueError("Name must not be empty.")
    if len(name) > 255:
        raise ValueError("Name must not be longer than 255 characters.")
    return name


def validate_description(description: str) -> str:
    """
    Validates the description of an object.

    :param description: The description of the object.
    :return: The validated description.
    """
    if description and len(description) > 1024:
        raise ValueError("Description must not be longer than 1024 characters.")
    return description
