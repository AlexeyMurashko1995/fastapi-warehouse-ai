# AI-Powered Warehouse Hub & Parcel Tracker 📦🤖

A production-ready backend service built with FastAPI and SQLModel, integrated with Mistral AI for automated real-time parcel classification and warehouse management.

## 🎯 Goal
This project demonstrates the design and deployment of a REST API for logistics management, combining relational database integrity with European Large Language Models (LLMs) to automate real-time business workflows.

## 📊 Core Capabilities
- **Real-Time AI Classification:** Automatically categorizes warehouse items using the `mistral-small-latest` model based on unstructured text descriptions.
- **Relational Integrity:** Implements a robust One-to-Many relationship between logistics Hubs and Parcels using SQLModel.
- **Enterprise-Grade Error Handling:** Features strict network and API error catches (`httpx.HTTPError`) with defensive fallbacks, ensuring 100% server uptime even during external API downtime.

## 🛠 Tech Stack
- **Language:** Python 3.x
- **Framework:** `FastAPI` (REST API)
- **ORM / Validation:** `SQLModel` (Built on top of `SQLAlchemy` & `Pydantic`)
- **Database:** `SQLite` (Relational Schema & Foreign Keys)
- **AI Integration:** `Mistral AI API` via asynchronous `HTTPX` client (`httpx.AsyncClient`)
- **Configuration & Auth:** `Python-dotenv` (Secure environment variables), Role-tailored response schemas

## 📁 Project Structure
- `hub_tracking.py`: The core application containing database models, API endpoints, and the AI integration logic.
- `.env`: Secure storage for API tokens (Excluded from Git for security).
- `.gitignore`: Configured to protect sensitive files (`.env`, local `.db` files).

## 🚀 Key Technical Features
- **Strict Prompt Engineering:** Utilizes dedicated system prompt constraints to force the LLM to return exactly one lowercase token (`electronics`, `clothes`, `food`, or `unknown`) with zero conversational overhead.
- **Advanced Querying & Pagination:** Out-of-the-box support for warehouse data filtering by city and parcel weight, utilizing `limit` and `offset` for high-performance database pagination.
- **Data Security:** Complete decoupling of system secrets from the source code via environment variables.
- **Tailored Response Schemas:** Uses distinct read models (`HubRead`, `ParcelRead`, `ParcelCourierRead`) to control data visibility depending on the user's role (e.g., restricted view for couriers).

## 📈 Roadmap
- [x] Design SQLModel Relational Schemas (Hub & Parcel)
- [x] Build RESTful API Endpoints with Filters & Pagination
- [x] Secure API Key Management via `.env`
- [x] Integrate Mistral AI for Real-Time Item Sorter via `httpx`
- [x] Implement Graceful Fallbacks for External API Failures
- [x] Implement Role-Based Response Schemas (`ParcelCourierRead`)
- [ ] Implement async database sessions for higher concurrency
- [ ] Add unit tests for endpoints using `pytest`