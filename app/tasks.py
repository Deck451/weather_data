
from celery import Celery
import httpx


task_queue: Celery = Celery(
    "tasks",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="redis://redis:6379/0",
)


@task_queue.task
def fetch_weather(city: str) -> dict:
    """Fetch weather data for a specific city."""

    try:
        # First, get the latitude and longitude of the city
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = httpx.get(geo_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        if not geo_data.get("results"):
            return {
                "success": False, 
                "error": "City not found."
            }
        
        # Extract latitude and longitude and get weather data
        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]
        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}&current_weather=true"
        )
        weather_response = httpx.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        return {
            "success": True,
            "city": city,
            "latitude": latitude,
            "longitude": longitude,
            "weather": weather_data["current_weather"],
        }
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }
