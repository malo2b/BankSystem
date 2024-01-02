# bksys_gateway_client

Gateway whose role is to orchestrate different micro-services by carrying business logic

## Setup project

requirements:
- python 3.11
- poetry

### Install dependencies and load environment
```
poetry install && poetry shell
```

### Run application for development
```
uvicorn bksys_gateway_client:app --reload
```

## Lint project
```
poetry run flake8
```
