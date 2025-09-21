# License Plate Recognition and Helmet Detection System

## Project Overview

This project provides an advanced AI-powered system for license plate recognition (LPR) and helmet detection. It includes a FastAPI-based web application, a Python desktop application, and a Next.js frontend, all leveraging YOLOv5 machine learning models for real-time traffic safety monitoring.

## Architecture Overview

Our system is designed with a microservices-like architecture, separating concerns for better scalability and maintainability. It consists of three main deployable components:

1.  **Frontend (Next.js on Vercel)**: Serves the user interface.
2.  **FastAPI Backend (Docker Container on Render)**: Handles API requests, database interactions, and orchestrates ML model inferences.
3.  **ML Models Service (Docker Container on Render)**: Provides an API for running license plate and helmet detection, consuming input from the Django backend.

```mermaid
graph TD
    User[User] --> Frontend[Frontend (Next.js on Vercel)]
    Frontend --> FastAPIAPI[FastAPI Backend (Render)]
    FastAPIAPI --> MLModelService[ML Models Service (Render)]
    FastAPIAPI --> PostgreSQL[PostgreSQL Database (Managed Service)]
    MLModelService --> ObjectDetection[YOLOv5 Model for Object Detection]
    MLModelService --> OCR[EasyOCR for Text Recognition]

    subgraph Render
        FastAPIAPI
        MLModelService
    end

    subgraph Vercel
        Frontend
    end

    style Frontend fill:#333,stroke:#6C6,stroke-width:2px,color:#fff
    style FastAPIAPI fill:#333,stroke:#6CF,stroke-width:2px,color:#fff
    style MLModelService fill:#333,stroke:#F6C,stroke-width:2px,color:#fff
    style PostgreSQL fill:#333,stroke:#FC6,stroke-width:2px,color:#fff
    style User fill:#000,stroke:#AAA,stroke-width:2px,color:#fff
    style ObjectDetection fill:#444,stroke:#C6C,stroke-width:1px,color:#fff
    style OCR fill:#444,stroke:#C6C,stroke-width:1px,color:#fff
```

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

*   Python 3.8+
*   Node.js (LTS version)
*   npm or yarn
*   Docker (for containerized deployments)

### 1. Clone the repository

```bash
git clone https://github.com/realranjan/licenece-pate-ai.git
cd licenece-pate-ai
```

### 2. ML Models Setup

### 3. Frontend Setup (Next.js)

### 4. Desktop Application Setup

## Deployment

This section outlines the steps to deploy each component of the system to their respective platforms.

### 1. Frontend Deployment (Vercel)

Your Next.js frontend will be deployed on Vercel.

1.  **Sign up/Log in to Vercel**: Go to [vercel.com](https://vercel.com/) and sign up or log in with your GitHub account.
2.  **Import Project**: From your Vercel dashboard, click 'Add New...' > 'Project' and select your `licenece-pate-ai` GitHub repository.
3.  **Configure Project**:
    *   **Root Directory**: Set this to `frontend/` (or the path to your Next.js project if it's not directly in `frontend/`).
    *   **Build Command**: Vercel usually auto-detects Next.js, but if needed, it's `npm run build` or `yarn build`.
    *   **Output Directory**: `dist` or `.next` (Vercel typically handles this automatically for Next.js).
    *   **Environment Variables**: You will need to add environment variables for your FastAPI backend API URL (e.g., `NEXT_PUBLIC_FASTAPI_API_URL`).
4.  **Deploy**: Click 'Deploy'. Vercel will build and deploy your frontend. It will provide you with a live URL.

### 2. FastAPI Backend Deployment (Render)

Your FastAPI backend will be deployed as a Docker container on Render.

1.  **Sign up/Log in to Render**: Go to [render.com](https://render.com/) and sign up or log in.
2.  **Create a New Web Service**: In your Render dashboard, click 'New' > 'Web Service'.
3.  **Connect to GitHub**: Connect your `licenece-pate-ai` GitHub repository.
4.  **Configure Web Service**:
    *   **Name**: Choose a name for your service (e.g., `fastapi-backend`).
    *   **Root Directory**: `web_app/`
    *   **Runtime**: `Docker`
    *   **Build Command**: Leave empty (Docker will handle building with the Dockerfile).
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT` (Render injects the `PORT` environment variable).
    *   **Environment Variables**: Add necessary environment variables, such as `ML_MODELS_SERVICE_URL` (the URL of your deployed ML Models service), and any database-related variables if your FastAPI app interacts with a database (e.g., `DATABASE_URL`).
5.  **Create a PostgreSQL Database (Optional)**: If your FastAPI backend requires a database, create a new PostgreSQL database on Render and link it to your web service. Render will automatically provide the `DATABASE_URL` environment variable.
6.  **Deploy**: Click 'Create Web Service'. Render will build your Docker image and deploy your FastAPI application.

### 3. ML Models Service Deployment (Render)

Your ML Models service will also be deployed as a Docker container on Render.

1.  **Create a New Web Service**: In your Render dashboard, click 'New' > 'Web Service'.
2.  **Connect to GitHub**: Connect your `licenece-pate-ai` GitHub repository.
3.  **Configure Web Service**:
    *   **Name**: Choose a name for your service (e.g., `ml-models-service`).
    *   **Root Directory**: `ml_models/`
    *   **Runtime**: `Docker`
    *   **Build Command**: Leave empty.
    *   **Start Command**: `python detection/api.py` (Assuming you'll create an API endpoint script here, e.g., `ml_models/detection/api.py` that serves your models via Flask/FastAPI, or you can use the default command in the Dockerfile if it's a simple script). *Note: You might need to adjust this command if your ML models are served differently.*
    *   **Environment Variables**: Any specific environment variables for your ML models (e.g., model paths, confidence thresholds).
4.  **Deploy**: Click 'Create Web Service'. Render will build your Docker image and deploy your ML Models service.

## Contributing

## License
