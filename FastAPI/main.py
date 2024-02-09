from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, for development only
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

openai.api_key = "apiKeyremoved"

class MarketResearchRequest(BaseModel):
    details: str

class EmailOutreachRequest(BaseModel):
    target_details: str
    context: str
    points_to_address: str

class SocialMediaPostRequest(BaseModel):
    topic: str
    target_audience: str
    specifics: str

@app.post("/market-research")
async def market_research(request: MarketResearchRequest):
    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Generate a market research report on: {request.details}",
            max_tokens=500
        )
        return {"report": response.choices[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-email")
async def generate_email(request: EmailOutreachRequest):
    try:
        prompt = f"Create a personalized email sequence for: {request.target_details}. Context: {request.context}. Key points: {request.points_to_address}"
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        return {"email": response.choices[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/social-media-post")
async def social_media_post(request: SocialMediaPostRequest):
    try:
        prompt = f"Generate a social media post about {request.topic} for {request.target_audience}. Include: {request.specifics}"
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150
        )
        return {"post": response.choices[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from mangum import Mangum
handler = Mangum(app)
