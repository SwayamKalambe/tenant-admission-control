from core.database import engine, Base

from api.models import *
from api.admission import *


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    create_tables()
