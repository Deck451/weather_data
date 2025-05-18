"""Unit tests for the main module."""

import uuid
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
import pytest

from app.main import app


client = TestClient(app)


def test_get_weather() -> None:
    """Test /weather endpoint handler."""
    fake_task_id: str = f"{uuid.uuid4()}"

    with patch("app.main.fetch_weather") as mock_fetch_weather:
        mock_task: MagicMock = MagicMock()
        mock_task.id = fake_task_id
        mock_fetch_weather.delay.return_value = mock_task

        response: JSONResponse = client.post(
            "/weather",
            json={"city": f"{uuid.uuid4()}"},
        )

        assert response.status_code == 200
        assert response.json().get("task_id") == fake_task_id


@pytest.mark.parametrize(
    "state",
    [
        f"{uuid.uuid4()}",
        "SUCCESS",
    ],
)
def test_get_weather_status(state: str) -> None:
    """Test /weather/{task_id} endpoint handler."""
    with patch("app.main.fetch_weather") as mock_fetch_weather:
        mock_result: MagicMock = MagicMock()
        mock_result.state = state
        if state == "SUCCESS":
            mock_result.result = {f"{uuid.uuid4()}": f"{uuid.uuid4()}"}
        mock_fetch_weather.AsyncResult.return_value = mock_result

        response: JSONResponse = client.get(
            f"/weather/{uuid.uuid4()}",
        )

        assert response.status_code == 200
        if state == "SUCCESS":
            assert response.json().get("result") == mock_result.result
        else:
            assert response.json().get("state") == state
