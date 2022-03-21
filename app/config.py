from sqlmodel import Session, create_engine
from dotenv import load_dotenv
from os import getenv


load_dotenv(override=True)

SECRET_KEY = getenv("SECRET_KEY")
DATABASE_URL = getenv("DATABASE_URL")
DEV = getenv("DEV")
engine = create_engine(DATABASE_URL, echo=True if DEV == "1" else False)


def get_session():
    with Session(engine) as session:
        yield session

