import json
from httpx import HTTPStatusError
import pytest
from app.adapters.data_adapter import DataAdapter
from pytest_httpx import HTTPXMock

@pytest.mark.asyncio
async def test_fetch_and_transform_data_csv(httpx_mock: HTTPXMock):
    csv_content = "name,age,city\nJohn,30,New York\nJane,25,London"
    httpx_mock.add_response(url="https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv ", text=csv_content)

    data = await DataAdapter.fetch_and_transform_data("https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv ", "csv")
    expected_data = [
        {"name": "John", "age": "30", "city": "New York"},
        {"name": "Jane", "age": "25", "city": "London"}
    ]

    assert data == expected_data

@pytest.mark.asyncio
async def test_fetch_and_transform_data_json(httpx_mock):
    json_content = '[{"name": "John", "age": 30, "city": "New York"}, {"name": "Jane", "age": 25, "city": "London"}]'
    httpx_mock.add_response(url="https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json", text=json_content)

    data = await DataAdapter.fetch_and_transform_data("https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json", "json")
    expected_data = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Jane", "age": 25, "city": "London"}
    ]

    assert data == expected_data


def test_transform_csv():
    csv_content = "name,age,city\nJohn,30,New York\nJane,25,London"
    result = DataAdapter.transform_csv(csv_content)
    expected = [
        {"name": "John", "age": "30", "city": "New York"},
        {"name": "Jane", "age": "25", "city": "London"}
    ]

    assert result == expected


def test_transform_json():
    json_content = '[{"name": "John", "age": 30, "city": "New York"}, {"name": "Jane", "age": 25, "city": "London"}]'
    result = DataAdapter.transform_json(json_content)
    expected = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Jane", "age": 25, "city": "London"}
    ]

    assert result == expected

async def test_fetch_and_transform_data_invalid_url(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="http://invalid-url.com", status_code=404)

    with pytest.raises(HTTPStatusError):
        await DataAdapter.fetch_and_transform_data("http://invalid-url.com", "csv")


def test_transform_json_invalid_format():
    invalid_json_content = '{"name": "John", "age": 30, "city": "New York",}'  # Trailing comma is invalid

    with pytest.raises(json.JSONDecodeError):
        DataAdapter.transform_json(invalid_json_content)


@pytest.mark.asyncio
async def test_fetch_and_transform_data_csv_with_bom(httpx_mock):
    csv_content = b"\ufeffname,age,city\nJohn,30,New York\nJane,25,London"
    httpx_mock.add_response(url="http://test-csv-url.com", text=csv_content)

    data = await DataAdapter.fetch_and_transform_data("http://test-csv-url.com", "csv")
    expected_data = [
        {"name": "John", "age": "30", "city": "New York"},
        {"name": "Jane", "age": "25", "city": "London"}
    ]

    assert data == expected_data
