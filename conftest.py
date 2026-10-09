import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from httpx import ASGITransport, AsyncClient
from hub_tracking import app, get_session


test_engine = create_engine(url="sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)


def override_get_session():
    with Session(test_engine) as session:
        yield session


@pytest.fixture(autouse=True)
def setup():
    SQLModel.metadata.create_all(test_engine)
    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
async def get_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client