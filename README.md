# weather_data POC

A proof-of-concept project demonstrating FastAPI with Celery, RabbitMQ, and Redis using Docker Compose.

## Quick Start

```sh
git clone https://github.com/deck451/celery_poc.git
cd celery_poc
docker compose up --build
```

## API Usage

- **POST** `/weather`  
  Request body: `{ "city": "Berlin" }`

- **GET** `/weather/{task_id}`  
  Returns weather result or task status.

## Services

- FastAPI app: [http://localhost:8000](http://localhost:8000)
- RabbitMQ management: [http://localhost:15672](http://localhost:15672) (user: guest/guest)
