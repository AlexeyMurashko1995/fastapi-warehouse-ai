# AI-Powered Warehouse Hub & Parcel Tracker 📦🤖

A production-ready backend service built with FastAPI and SQLModel, integrated with Mistral AI for automated real-time parcel classification and warehouse management.

## 🎯 Goal
My goal is to find and secure an IT backend / AI engineering position in Summer 2026. This project demonstrates my ability to design relational databases, build clean RESTful APIs, and integrate advanced European Large Language Models (LLMs) into business workflows.

## 📊 Core Capabilities
- **Real-Time AI Classification:** Automatically categorizes warehouse items using the `mistral-small-latest` model based on text descriptions.
- **Relational Integrity:** Implements a robust One-to-Many relationship between logistics Hubs and Parcels.
- **Enterprise-Grade Error Handling:** Features strict network and API error catches, ensuring 100% server uptime even during external API downtime.

## 🛠 Tech Stack
- **Language:** Python 3.x
- **Framework:** `FastAPI` (Asynchronous REST API)
- **ORM / Database:** `SQLModel` (SQLAlchemy & Pydantic hybrid) with SQLite
- **AI Integration:** `Mistral AI API` via `Requests`
- **Configuration:** `Python-dotenv` (Secure environment variables)

## 📁 Project Structure
- `hub_tracking.py`: The core application containing database models, API endpoints, and the AI integration logic.
- `.env`: Secure storage for API tokens (Excluded from Git for security).
- `.gitignore`: Configured to protect sensitive files (`.env`, local `.db` files).

## 🚀 Key Technical Features
- **Strict Prompt Engineering:** Utilizes dedicated system prompt constraints to force the LLM to return exactly one lowercase token (`electronics`, `clothes`, `food`, or `unknown`) with zero conversational overhead.
- **Advanced Querying & Pagination:** Out of the box support for warehouse data filtering by city and parcel weight, utilizing `limit` and `offset` for high-performance database pagination.
- **Data Security:** Complete decoupling of system secrets from the source code via environment variables.
- **Tailored Response Schemas:** Uses distinct read models (`HubRead`, `ParcelRead`, `ParcelCourierRead`) to control data visibility depending on the user's role (e.g., restricted view for couriers).

## 📈 Roadmap
- [x] Design SQLModel Relational Schemas (Hub & Parcel)
- [x] Build RESTful API Endpoints with Filters & Pagination
- [x] Secure API Key Management via `.env`
- [x] Integrate Mistral AI for Real-Time Item Sorter
- [x] Implement Graceful Fallbacks for External API Failures
- [ ] Implement async database sessions for higher concurrency
- [ ] Add unit tests for endpoints using `pytest`