from sqlalchemy import create_engine
from models import Base
import os
from dotenv import load_dotenv

load_dotenv()

# Update the connection string as needed
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set.")
engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(engine)

print("All tables created successfully.") 