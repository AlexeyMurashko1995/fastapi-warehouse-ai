import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_get_hubs(get_client):
    response = await get_client.get(url="/hubs")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_hub(get_client):
    response = await get_client.post(url="/hubs", json={"name": "Gdanski", "city": "Gdansk"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "name": "Gdanski", "city": "Gdansk"}


@pytest.mark.asyncio
async def test_read_single_hub_success(get_client):
    request = await get_client.post(url="/hubs", json={"name": "Gdanski", "city": "Gdansk"})
    response = await get_client.get(url="/hubs/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "name": "Gdanski", "city": "Gdansk"}