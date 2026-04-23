from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import os
import time

app = FastAPI()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ENDPOINT_NAME = os.getenv("ENDPOINT_NAME", "")
TEAM_NAME = os.getenv("TEAM_NAME", "fraud-detection")
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")

runtime = boto3.client("sagemaker-runtime", region_name=AWS_REGION)

request_count = 0
start_time = time.time()

class PredictionRequest(BaseModel):
    features: list[float]

@app.get("/health")
def health():
    return {
        "status": "ok",
        "team": TEAM_NAME,
        "version": MODEL_VERSION,
        "requests_served": request_count
    }

@app.get("/ready")
def ready():
    if not ENDPOINT_NAME:
        raise HTTPException(status_code=500, detail="ENDPOINT_NAME not configured")

    return {
        "status": "ready",
        "endpoint": ENDPOINT_NAME
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    global request_count

    try:
        payload = ",".join(map(str, request.features))

        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="text/csv",
            Body=payload
        )

        result = response["Body"].read().decode("utf-8").strip()

        request_count += 1

        return {
            "team": TEAM_NAME,
            "prediction": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))