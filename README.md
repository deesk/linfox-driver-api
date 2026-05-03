# Linfox Driver Management API

A RESTful CRUD API built with FastAPI to manage driver records for Linfox Melbourne logistics operations.

## What This Is

This API serves as the data management layer that complements the [Linfox RAG Chatbot](https://github.com/deesk/linfox-rag-chatbot-azure). The chatbot answers operational queries -- this API manages the structured driver data behind those answers.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/drivers` | List all drivers. Filter by `shift_type`, `roster_pattern`, `licence_class` |
| GET | `/drivers/{driver_id}` | Get a single driver by employee ID |
| POST | `/drivers` | Add a new driver |
| PUT | `/drivers/{driver_id}` | Partially update a driver record |
| DELETE | `/drivers/{driver_id}` | Deactivate a driver (soft delete) |

## Key Design Decisions

**Soft delete** -- deactivating a driver sets `is_active=False` rather than removing the record. Operational history is retained for NHVR compliance purposes.

**Computed licence expiry** -- `is_licence_expired` is calculated on every GET request by comparing `licence_expiry` against today's date. It is never stored -- always accurate.

**Filtering via query parameters** -- `/drivers?shift_type=night&licence_class=MC` rather than a separate `/filter` endpoint, which is REST standard.

## Tech Stack

- FastAPI
- Pydantic
- Python 3.13
- JSON file as data store (POC only -- no concurrency protection)

## Run Locally

```bash
git clone https://github.com/deesk/linfox-driver-api
cd linfox-driver-api
python -m venv venv
venv\Scripts\Activate.ps1
pip install fastapi uvicorn
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## Related

[Linfox RAG Chatbot](https://github.com/deesk/linfox-rag-chatbot-azure) -- domain-specific RAG chatbot built on Azure AI Foundry.