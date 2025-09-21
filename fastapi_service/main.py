from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import requests
from io import BytesIO
import base64

app = FastAPI()

ML_MODELS_SERVICE_URL = "http://localhost:5000" # TODO: Replace with your actual deployed ML Models service URL

@app.post("/detect-license-plate/")
async def detect_license_plate(file: UploadFile = File(...)):
    """
    Receives an image, forwards it to the ML Models service, and returns the detection results.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    try:
        image_data = await file.read()
        
        # Forward the image to the ML Models service
        # The ML Models service should have an endpoint to accept image data and return predictions
        ml_response = requests.post(
            f"{ML_MODELS_SERVICE_URL}/predict",
            files={"file": (file.filename, image_data, file.content_type)}
        )
        ml_response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        # Assuming the ML service returns JSON with detection results
        detections = ml_response.json()
        
        return JSONResponse(content={"filename": file.filename, "detections": detections})

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="ML Models service is unavailable.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error from ML Models service: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.get("/")
@app.head("/")  # Add this line to allow HEAD requests
async def root():
    return {"message": "Welcome to the FastAPI License Plate Detection API!"}
