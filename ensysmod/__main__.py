"""
This is the main file of project %name%.

It is invoked when someone runs python like:
    python -m %name%
"""
import uvicorn


def main():
    # noinspection PyTypeChecker
    uvicorn.run(app="ensysmod.app:app", host="0.0.0.0", port=8080, log_level="info", reload=True)


if __name__ == "__main__":
    main()
