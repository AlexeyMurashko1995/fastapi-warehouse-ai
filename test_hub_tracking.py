import pytest
from fastapi import status
from unittest.mock import patch

HUB_PAYLOAD = {"name": "Gdanski", "city": "Gdansk"}
PARCEL_PAYLOAD = {
    "tracking_number": "WA",
    "weight": 54.0,
    "description": "home",
    "hub_id": 1,
}


@pytest.mark.asyncio
async def test_get_hubs(get_client):
    response = await get_client.get(url="/hubs")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_hub(get_client):
    response = await get_client.post(url="/hubs", json=HUB_PAYLOAD)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, **HUB_PAYLOAD}


@pytest.mark.asyncio
async def test_read_single_hub_success(get_client):
    await get_client.post(url="/hubs", json=HUB_PAYLOAD)
    response = await get_client.get(url="/hubs/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, **HUB_PAYLOAD}


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
    await get_client.post(url="/hubs", json=HUB_PAYLOAD)
    await get_client.post(url="/parcels", json=PARCEL_PAYLOAD)
    response = await get_client.get(url="/parcels/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        **PARCEL_PAYLOAD,
        "category": "unknown",
    }


@pytest.mark.asyncio
async def test_delete_single_parcel_failure(get_client):
    response = await get_client.delete(url="/parcels/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Parcel not found"}


@pytest.mark.asyncio
async def test_delete_single_parcel_success(get_client):
    await get_client.post(url="/hubs", json=HUB_PAYLOAD)
    await get_client.post(url="/parcels", json=PARCEL_PAYLOAD)
    delete_response = await get_client.delete("/parcels/1")
    get_response = await get_client.get(url="/parcels/1")

    assert delete_response.status_code == status.HTTP_200_OK
    assert delete_response.json() == {
        "status": "success",
        "message": "Parcel 1 deleted successfully",
    }
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json() == {"detail": "Parcel not found"}


@pytest.mark.asyncio
async def test_read_single_parcel_courier_success(get_client):
    create_hub = await get_client.post("/hubs", json=HUB_PAYLOAD)
    create_parcel = await get_client.post("/parcels", json=PARCEL_PAYLOAD)
    response = await get_client.get("/parcels/1/public")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "tracking_number": "WA", "description": "home", "hub_id": 1}


@pytest.mark.asyncio
async def test_read_single_parcel_courier_failure(get_client):
    response = await get_client.get("/parcels/999/public")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Parcel not found"}


@pytest.mark.asyncio
async def test_create_parcel_success(get_client):
    request = await get_client.post(url="/hubs", json=HUB_PAYLOAD)
    with patch("hub_tracking.get_ai_category", return_value="electronics"):
        response = await get_client.post(url="/parcels", json=PARCEL_PAYLOAD)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["category"] == "electronics"
