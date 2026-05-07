import pytest

MARKET_ORDER = {
    "instrument": "DE000A0Q4RZ3",
    "type": "market",
    "quantity": 10,
    "side": "buy",
}


@pytest.mark.asyncio
async def test_create_market_order(client, mocker):
    mocker.patch("services.order_service.place_order_task.delay")

    resp = await client.post("/orders", json=MARKET_ORDER)

    assert resp.status_code == 201
    data = resp.json()
    assert data["instrument"] == "DE000A0Q4RZ3"
    assert data["status"] == "pending"
    assert data["limit_price"] is None
    assert "id" in data


@pytest.mark.asyncio
async def test_create_limit_order(client, mocker):
    mocker.patch("services.order_service.place_order_task.delay")

    resp = await client.post("/orders", json={
        **MARKET_ORDER,
        "type": "limit",
        "limit_price": 42.5,
    })

    assert resp.status_code == 201
    assert resp.json()["limit_price"] == 42.5


@pytest.mark.asyncio
async def test_limit_order_without_price(client):
    resp = await client.post("/orders", json={**MARKET_ORDER, "type": "limit"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_market_order_with_price(client):
    resp = await client.post("/orders", json={**MARKET_ORDER, "limit_price": 10.0})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_invalid_side(client):
    resp = await client.post("/orders", json={**MARKET_ORDER, "side": "hold"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_task_is_enqueued(client, mocker):
    mock = mocker.patch("services.order_service.place_order_task.delay")

    resp = await client.post("/orders", json=MARKET_ORDER)

    assert resp.status_code == 201
    mock.assert_called_once_with(resp.json()["id"])
