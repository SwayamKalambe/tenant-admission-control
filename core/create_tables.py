from core.database import engine, Base
from api.models import *

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")