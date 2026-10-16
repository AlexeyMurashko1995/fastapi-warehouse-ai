import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_hubs(get_client):
    response = await get_client.get(url="/hubs")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_hub(get_client):
    response = await get_client.post(
        url="/hubs", json={"name": "Gdanski", "city": "Gdansk"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "name": "Gdanski", "city": "Gdansk"}


@pytest.mark.asyncio
async def test_read_single_hub_success(get_client):
    await get_client.post(
        url="/hubs", json={"name": "Gdanski", "city": "Gdansk"}
    )
    response = await get_client.get(url="/hubs/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "name": "Gdanski", "city": "Gdansk"}


@pytest.mark.asyncio
async def test_read_single_hub_failure(get_client):
    response = await get_client.get("/hubs/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Hub not found"}


@pytest.mark.asyncio
async def test_read_parcels_data(get_client):
    response = await get_client.get(url="/parcels")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_single_parcel_failure(get_client):
    response = await get_client.get("/parcels/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Parcel not found"}


@pytest.mark.asyncio
async def test_read_single_parcel_success(get_client):
    await get_client.post(
        url="/hubs", json={"name": "Gdanski", "city": "Gdansk"}
    )
    await get_client.post(
        url="/parcels",
        json={
            "tracking_number": "WA",
            "weight": 54.0,
            "description": "home",
            "hub_id": 1,
        },
    )
    response = await get_client.get(url="/parcels/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "tracking_number": "WA",
        "weight": 54.0,
        "description": "home",
        "category": "unknown",
        "hub_id": 1,
    }


@pytest.mark.asyncio
async def test_delete_single_parcel_failure(get_client):
    response = await get_client.delete(url="/parcels/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Parcel not found"}


@pytest.mark.asyncio
async def test_delete_single_parcel_success(get_client):
    await get_client.post(
        url="/hubs", json={"name": "Gdanski", "city": "Gdansk"}
    )
    await get_client.post(
        url="/parcels",
        json={
            "tracking_number": "WA",
            "weight": 54.0,
            "description": "home",
            "hub_id": 1,
        },
    )
    delete_response = await get_client.delete("/parcels/1")
    get_response = await get_client.get(url="/parcels/1")

    assert delete_response.status_code == status.HTTP_200_OK
    assert delete_response.json() == {
        "status": "success",
        "message": "Parcel 1 deleted successfully",
    }
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json() == {"detail": "Parcel not found"}