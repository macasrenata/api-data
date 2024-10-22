import csv
import json
import httpx
from io import StringIO

class DataAdapter:
    @staticmethod
    async def fetch_and_transform_data(url: str, data_format: str) -> list[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if data_format == "csv":
            return DataAdapter.transform_csv(response.text)
        elif data_format == "json":
            return DataAdapter.transform_json(response.text)

    @staticmethod
    def transform_csv(data: str) -> list[dict]:
        if data.startswith('\ufeff'):
            data = data[1:]

        csv_data = csv.DictReader(StringIO(data))
        return [row for row in csv_data]

    @staticmethod
    def transform_json(data: str) -> list[dict]:
        if data.startswith('\ufeff'):
            data = data[1:]

        return json.loads(data)
