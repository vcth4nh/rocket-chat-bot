from dotenv import load_dotenv
import os
load_dotenv('.env')
load_dotenv('../mongo.env')

DATABASE_NAME=os.getenv('MONGO_INITDB_DATABASE')
MONGO_INITDB_ROOT_USERNAME=os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD=os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGO_HOST=os.getenv('MONGO_HOST')
MONGO_PORT=os.getenv('MONGO_PORT')

MONGO_URI = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
# MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{DATABASE_NAME}"

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPI_MINUTES")