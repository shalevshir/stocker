from sqlalchemy import create_engine
from models import Base

# Update the connection string as needed
DATABASE_URL = "postgresql+psycopg2://stocker:stockerpass@localhost:54320/stockerdb"

engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(engine)

print("All tables created successfully.") 