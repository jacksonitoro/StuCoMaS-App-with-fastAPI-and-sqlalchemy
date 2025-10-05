# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sprint2.database import Base
from sprint2.api import app, get_db

# --- Use a shared in-memory SQLite database ---
SQLALCHEMY_DATABASE_URL = "sqlite:///file:memdb1?mode=memory&cache=shared"

# Create a shared engine (important!)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False, "uri": True}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables once in the shared memory DB
Base.metadata.create_all(bind=engine)

# --- Dependency override to use test DB ---
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)



# --- Test client fixture ---
@pytest.fixture(scope="session")
def client():
    # Recreate all tables before each test for isolation
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
