# BankSystem

## Description

BankSystem is a project that aims to create simple a banking system with a microservice architecture.

## Installation

### 🐳 With docker

requirements:
- docker
- docker-compose

```bash
docker-compose up --build
```

🔗 links:
- [localhost:11000/docs](http://localhost:11000) - bksys_gateway_client swagger
- [localhost:11001/docs](http://localhost:11001) - bksys_account_ms swagger
- [localhost:11002/docs](http://localhost:11002) - bksys_operations_rule_ms swagger
- [localhost:11003/docs](http://localhost:11003) - bksys_transaction_ms swagger
- [localhost:3000](http://localhost:3000) - grafana
- [localhost:9090](http://localhost:9090) - prometheus

### 🐍 With python

requirements:
- python 3.11
- poetry

```bash
poetry install && poetry shell
```

uvicorn
```bash
uvicorn service_name:app --reload --port 8080
```
python
```bash
python -m service_name
```