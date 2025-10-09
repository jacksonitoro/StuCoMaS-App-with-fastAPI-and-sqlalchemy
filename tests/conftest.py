import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sprint2.database import Base
from sprint2.api import app, get_db

# ============================================================
# 🧩 Test Database Setup (shared in-memory)
# ============================================================

SQLALCHEMY_DATABASE_URL = "sqlite:///file:memdb1?mode=memory&cache=shared"

# ✅ Shared engine for consistent memory state
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False, "uri": True}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ============================================================
# 🧩 Override the main app DB dependency
# ============================================================

def override_get_db():
    """Provide a fresh database session for each test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# ============================================================
# 🧹 Fixtures for Test Isolation
# ============================================================

@pytest.fixture(scope="function", autouse=True)
def clean_test_db():
    """
    Automatically runs before each test.
    Drops and recreates all tables for total isolation.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """
    Provides a new FastAPI TestClient for each test,
    ensuring DB and app state are clean.
    """
    with TestClient(app) as c:
        yield c
