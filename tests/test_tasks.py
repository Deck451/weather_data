"""Unit tests for the tasks module."""

import uuid
from unittest.mock import patch, MagicMock

import pytest

from app.tasks import fetch_weather


@pytest.mark.parametrize(
    "outcome",
    [
        "success",
        "failure",
        "exception",
    ],
)
def test_fetch_weather(outcome: str) -> None:
    """Test fetch_weather task."""

    city: str = f"{uuid.uuid4()}"
    exception_message: str = f"{uuid.uuid4()}"
    geo_data: dict = {"results": []}
    if outcome == "success":
        geo_data["results"] = [
            {
                "latitude": 12.34,
                "longitude": 56.78,
            }
        ]

    weather_data: dict = {
        "current_weather": {
            "temperature": 20,
            "windspeed": 5,
        }
    }

    with patch("httpx.get") as mock_get:
        mock_geo_response: MagicMock = MagicMock()
        mock_geo_response.json.return_value = geo_data
        mock_geo_response.raise_for_status.return_value = None

        mock_weather_response: MagicMock = MagicMock()
        mock_weather_response.json.return_value = weather_data
        mock_weather_response.raise_for_status.return_value = None

        if outcome == "exception":
            mock_get.side_effect = Exception(exception_message)
        else:
            mock_get.side_effect = [mock_geo_response, mock_weather_response]

        result = fetch_weather(city)

        if outcome == "success":
            assert result["success"] is True
            assert result["city"] == city
            assert result["latitude"] == geo_data["results"][0]["latitude"]
            assert result["longitude"] == geo_data["results"][0]["longitude"]
            assert result["weather"] == weather_data["current_weather"]
        else:
            assert "error" in result
            if outcome == "failure":
                assert "City not found." in result["error"]
            else:
                assert exception_message in result["error"]
