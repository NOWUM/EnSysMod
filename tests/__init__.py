import os

# Override env variables
os.environ['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
os.environ['SERVER_NAME'] = "Counter Test"
