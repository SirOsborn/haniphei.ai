from db.tables import User, Document, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set. Please set it before running this script.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

if __name__ == "__main__":
    session = SessionLocal()
    session.query(Document).delete()
    session.query(User).delete()
    session.commit()
    session.close()
    print("All users and documents deleted.")
