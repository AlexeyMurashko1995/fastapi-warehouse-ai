import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from httpx import ASGITransport, AsyncClient
from hub_tracking import app, get_session


test_engine = create_engine(url="sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)