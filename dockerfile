# =======================
# 1. Build React frontend
# =======================
FROM node:18 AS frontend-builder

WORKDIR /frontend
COPY React/finance-app/package*.json ./
RUN npm install
COPY React/finance-app/ ./
RUN npm run build

# =======================
# 2. Build FastAPI backend
# =======================
FROM python:3.11-slim AS backend

WORKDIR /app

# Install Python dependencies
COPY FastAPI/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI backend
COPY FastAPI/ .

# Copy built frontend into backend static folder
COPY --from=frontend-builder /frontend/build ./static

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
