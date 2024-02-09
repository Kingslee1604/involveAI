from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import boto3
import json

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, for development only
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Retrieve API key from AWS Secrets Manager
def get_secret():
    secret_name = "openAI_API_Key"
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

# Set openai.api_key using the retrieved API key
openai.api_key = get_secret()

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
        api_key = get_secret()
        try:
            api_key = json.loads(api_key)["openai_key"]  # Use the correct key here
        except json.JSONDecodeError:
            pass  # The secret was not in JSON format, so use it as-is
        openai.api_key = api_key

        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Generate a market research report on: {request.details}",
            max_tokens=500
        )
        return {"report": response.choices[0].text}
    except openai.Error as openai_error:
        # OpenAI-specific error handling
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(openai_error)}")
    except json.JSONDecodeError as json_error:
        # JSON parsing error
        raise HTTPException(status_code=500, detail=f"JSON decode error: {str(json_error)}")
    except boto3.exceptions.Boto3Error as boto_error:
        # AWS SDK-specific error handling
        raise HTTPException(status_code=500, detail=f"AWS Boto3 error: {str(boto_error)}")
    except Exception as e:
        # Generic error handling
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

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
