# Stage 1: Build React frontend
FROM node:18 AS frontend-build
WORKDIR /frontend
COPY React/finance-app/package*.json ./
RUN npm install
COPY React/finance-app/ ./
RUN npm run build

# Stage 2: Build FastAPI backend
FROM python:3.11-slim AS backend
WORKDIR /app

# Install FastAPI dependencies
COPY FastAPI/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY FastAPI/ .

# Copy frontend build into FastAPI static folder
COPY --from=frontend-build /frontend/build ./static


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

