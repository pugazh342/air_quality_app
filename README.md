# 🌍 Air Quality Monitoring & Prediction Web App

## 📌 Project Overview

This project is a comprehensive web application for monitoring and predicting air quality. It provides:

- Real-time Air Quality Index (AQI) data
- Historical trends
- Weather information
- Future AQI predictions

All data is presented through a responsive and interactive user interface.

The backend is built using **FastAPI**, and the frontend (planned) will use **React.js**.

---

## ⚙️ Tech Stack

### 🔧 Backend

- **Framework**: Python 3.10, FastAPI
- **HTTP Client**: `httpx`
- **Configuration**: `pydantic-settings`, `python-dotenv`
- **External APIs Integrated**:
  - OpenAQ (Air Quality Data)
  - OpenWeatherMap (Weather Data)
  - Mapbox (Geocoding)
- **Authentication**: Firebase Admin SDK (`firebase-admin`)
- **Database (Planned)**: PostgreSQL + TimescaleDB (via SQLAlchemy, Alembic)
- **Async Tasks (Planned)**: Celery + Redis
- **ML (Planned)**: TensorFlow or PyTorch

### 💻 Frontend (Planned)

- **Framework**: React.js
- **Styling**: Tailwind CSS
- **Routing**: React Router
- **Data Visualization**: Recharts, Leaflet.js
- **HTTP Client**: Axios

---

## 🚀 Project Setup

### ✅ Prerequisites

- Python 3.10
- Git
- (Optional) Docker Desktop — for PostgreSQL + TimescaleDB
- (Frontend - Future) Node.js & npm/Yarn

---

### 🔨 Backend Setup

```bash
# Clone the Repository
git clone https://github.com/your-username/air_quality_app.git
cd air_quality_app

# Create & Activate Virtual Environment
python -m venv venv
# Windows:
.env\Scriptsctivate
# macOS/Linux:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
# Or install manually if needed:
pip install fastapi uvicorn[standard] httpx pydantic-settings python-dotenv firebase-admin python-multipart
```

---

### 🔐 Environment Variables

Create a `.env` file in the root directory. Use `.env.example` as a template.

Fill in your keys:

```env
OPENWEATHER_API_KEY=your_key
MAPBOX_ACCESS_TOKEN=your_token
FIREBASE_SERVICE_ACCOUNT_PATH=/absolute/path/to/serviceAccountKey.json

POSTGRES_USER=aq_user
POSTGRES_PASSWORD=aq_password
POSTGRES_DB=aq_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

### ▶️ Run the Server

```bash
uvicorn main:application --reload
# Visit: http://127.0.0.1:8000
```

---

## 🛢️ Database Setup (Manual Installation Recommended)

Due to Docker issues, manual installation is advised on Windows.

1. **Install PostgreSQL** (v15+)
2. **Install TimescaleDB**
3. **Create DB & User**

```sql
-- From psql:
CREATE DATABASE aq_db;
CREATE USER aq_user WITH PASSWORD 'aq_password';
GRANT ALL PRIVILEGES ON DATABASE aq_db TO aq_user;
\c aq_db
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

---

## 📐 Alembic Migrations (Pending)

Set up Alembic to generate tables. This is part of the next development milestone.

---

## 🔑 Current API Endpoints

View Swagger UI at:  
**[http://127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs)**

### ✅ Health Check

- `GET /api/v1/health`

### 🌫️ Air Quality (OpenAQ)

- `GET /api/v1/aqi/latest`
- `GET /api/v1/locations`
- `GET /api/v1/aqi/historical/{location_id}`

### 🌦️ Weather (OpenWeatherMap)

- `GET /api/v1/weather/current`
- `GET /api/v1/weather/forecast`

### 🗺️ Location (Mapbox)

- `GET /api/v1/geocode/forward`
- `GET /api/v1/geocode/reverse`

### 👤 Auth (Firebase)

- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/token` *(Placeholder)*
- `GET /api/v1/auth/me`

---

## 🚧 Development Roadmap

### 📌 Backend

- ✅ Core API Integrations
- 🔄 Complete database models & CRUD (SQLAlchemy)
- 🧠 Build & integrate ML model (AQI prediction)
- ⏱️ Add Celery + Redis for background tasks
- 📈 Real-time updates (Redis Pub/Sub + WebSockets)

### 🧑‍💻 Frontend (Phase 3)

- Scaffold React app
- Build UI components (MapView, Charts, AQICard, etc.)
- Implement pages (Dashboard, Alerts, Settings)
- Add Recharts + Leaflet maps

### 🧪 Integration & Testing (Phase 4)

- API connection to frontend
- Unit & integration testing
- Responsive design & accessibility

### ☁️ Deployment (Phase 5)

- Dockerize frontend & backend
- CI/CD via GitHub Actions
- Deploy on AWS/GCP/Azure
- Add monitoring/logging (ELK + Prometheus/Grafana)

### 🚀 Post-MVP Ideas (Phase 6)

- Advanced ML (spatio-temporal modeling)
- Crowdsourced sensor calibration
- Personal AQI history log
- Wearables and community features

---

## 🤝 Contributing

_(To be added: contribution guidelines, code of conduct, issue templates.)_

---

## 📄 License

_(To be added: MIT, Apache 2.0, or your preferred license.)_

---
