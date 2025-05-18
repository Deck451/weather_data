"""FastAPI application for weather data retrieval and status checking."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from celery.result import AsyncResult

from app.tasks import fetch_weather


app: FastAPI = FastAPI()


class WeatherRequest(BaseModel):
    """Model for weather request."""
    city: str


@app.post("/weather")
async def get_weather(request: WeatherRequest) -> JSONResponse:
    """Get the weather for a specific city."""
    task: AsyncResult = fetch_weather.delay(request.city)
    return JSONResponse(
        {
            "task_id": task.id,
        }
    )


@app.get("/weather/{task_id}")
async def get_weather_status(task_id: str) -> JSONResponse:
    """Check the status of the weather request."""
    result = fetch_weather.AsyncResult(task_id)
    if result.state == "SUCCESS":
        return JSONResponse(
            {
                "result": result.result,
            }
        )
    return JSONResponse(
        {
            "state": result.state,
        }
    )
