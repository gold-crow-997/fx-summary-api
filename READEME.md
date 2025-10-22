# FX Summary API ✅

Simple FastAPI microservice that fetches EUR→USD exchange rates from Franklinshar.dev API  
and computes percentage changes between start and end dates.

## 🚀 Endpoints
- http://localhost:8000/docs#/default/summary_summary_get
- http://localhost:8000/health
### **GET /health**
Returns `{ "status": "ok" }`

### **GET /summary**
Query Parameters:
- `start` (required) — e.g. `2025-07-01`
- `end` (required) — e.g. `2025-07-03`
- `breakdown` — optional (`daily` or `none`)

Example:
