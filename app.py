from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

class request_body(BaseModel):
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
model = joblib.load("model.sav")
sex_encoder = joblib.load("sex_encoder.pkl")
smoker_encoder = joblib.load("smoker_encoder.pkl")
encoder = joblib.load("ohe.pkl")

@app.get("/")
def read_root():
    return {"Hello": "World"}

def preprocess_features(features: request_body):
    sex = sex_encoder.transform([features.sex])[0]
    smoker = smoker_encoder.transform([features.smoker])[0]
    region = encoder.transform([[features.region]])[0]

    data = np.array([features.age, sex, features.bmi, features.children, smoker] + list(region))
    return data

templates = Jinja2Templates(directory="templates")

@app.get("/predict", response_class=HTMLResponse)
async def render_predict(request: Request):
    print("Rendering template...")
    return templates.TemplateResponse("index.html", {"request": request, "title": "Welcome to FastAPI"})

@app.post("/predict")
def predict(features: request_body):
    data = preprocess_features(features)
    res = model.predict([data])[0]
    return {"predicted_cost": round(res, 2)}