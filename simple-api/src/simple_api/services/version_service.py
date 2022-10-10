import os


def get_application_version():
    return os.environ.get("APP_VERSION", "Not found")
