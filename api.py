from typing import Union, Annotated
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi import HTTPException
from acp import buyer 
from PIL import Image
import shutil
import asyncio
import os
import jawline_math as jm
# Temporarily commenting out these imports for testing
# from acp import buyer
from utils import s3Helper

from gemini_evaluator.evaluator import analyze_facial_features
from formatters.response_formatter import format_sigma_analysis_report
from services.jawline_service import analyze_jawline
from services.gemini_service import analyze_facial_features_service
from services.file_service import save_and_upload_mesh_image, save_and_upload_analysis_text
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]


app = FastAPI()
shape_list = ["Round", "Long"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Temporarily commented out for testing
s3Helper = s3Helper.s3Helper()

# Simple File Upload logic from user (Change to fit ACP)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/evaluation/{key}")
def evaluation(request: Request, key: str):
    # generate presigned image from s3
    mesh_path = f"mesh-{key}"
    mesh_url = s3Helper.generate_presigned_url(mesh_path)
    
    # Download text from S3
    guidance_s3_key = f"guidance-{key}"
    evaluation_path_text = f"evaluation/guidance-{key}.txt"
    
    # Ensure evaluation directory exists
    os.makedirs("evaluation", exist_ok=True)
    
    # Download from S3 to local file
    s3Helper.download(guidance_s3_key, evaluation_path_text)

    with open(evaluation_path_text, 'r') as file:
        content = file.read()

    templates = Jinja2Templates(directory="templates")
    
    # Use the content we just read from the downloaded file
    guidance = content
    

        
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page_title": "Sigma boi",
            "heading": "Your Image & Analysis",
            "image_src": mesh_url, 
            "image_alt": "User submission",
            "caption": f"Uploaded locally from {mesh_url}",
            "text_content": guidance,
            "is_html": True,  # set True if you pass HTML in text_content
        }
    )

# API returns website URL for frontend redirect
# Frontend pulls image and text from S3 using presigned urls
# Added Request as param for html request for easy transition to actual host

@app.get("/mog")
async def mog(request: Request, image: str, prompt: str, unique_key: str) -> dict:
    try:
        print(f"Processing request for image: {image}")
        ## First process the image with your existing jawline detection
        # download image from s3
        uploaded_file = s3Helper.download(unique_key, f"{UPLOAD_FOLDER}/{unique_key}.png")
        if not os.path.exists(uploaded_file):
            print(f"Image not found: {uploaded_file}")
            return {"error": f"Image {image} not found"}
        
        # Perform jawline analysis
        jawline_result = analyze_jawline(uploaded_file)
        
        # Perform LLM facial feature analysis  
        other_features = analyze_facial_features_service(uploaded_file)
        
        # Format the response using dedicated formatter
        readable_response = format_sigma_analysis_report(
            jawline_shape=jawline_result.jawline_shape,
            jawline_assessment=jawline_result.jawline_assessment,
            other_features=other_features
        )
        
        # Save and upload files
        print("Analysis complete!")
        mesh_key, mesh_url = save_and_upload_mesh_image(jawline_result.output_image, unique_key)
        guidance_path = save_and_upload_analysis_text(readable_response, unique_key) 
        
        # Return website URL for frontend to redirect to (dynamic host)
        base_url = str(request.base_url).rstrip('/')
        website_url = f"{base_url}/evaluation/{unique_key}"
        return {"website_url": website_url, "mesh_key": mesh_key}
    except Exception as e:
        print(f"Error in /mog endpoint: {str(e)}")
        return {
            "error": "Internal server error",
            "details": str(e)
        }


@app.post("/upload")
async def upload(
        image: UploadFile, 
        key: Annotated[str, Form()], 
        prompt: Annotated[str, Form()]
    ) -> dict: 
    
    if not image or not image.filename: 
        return "Please send file"
    try: 
        file_content = await image.read()
        print(f"Upload - Key: {key}, Filename: {image.filename}")
        s3_image_url = s3Helper.upload_file_content(file_content, key, image.filename, prompt)
        print(f"Upload - Result URL: {s3_image_url}")
    except Exception as e:
        print(e)
        response_error: dict = {
            "error": True, "error messsage": e
        }
        return response_error
    else: 
        response_successful: dict = {
            "error": False, "image_url": s3_image_url 
        }
        return response_successful


@app.post("/call/buyer")
async def call_buyer(
        image: UploadFile, 
        prompt: Annotated[str, Form()]
        ) -> dict:
    UPLOAD_DIRECTORY = "local_images"
    if not image or not image.filename: 
        raise HTTPException(status_code=404, detail="Image not found")

    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    file_location = os.path.join(UPLOAD_DIRECTORY, image.filename)

     # Save the file content
    with open(file_location, "wb") as buffer:
            # Read the uploaded file in chunks and write to the local file
        while content := await image.read(1024 * 1024): # Read in 1MB chunks
            buffer.write(content)
    try:
        print("calling buyer")
        deliverable = asyncio.run(buyer.buyer(image_url=file_location, prompt=prompt))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
        return {
            "error": "Internal server error",
            "details": str(e)
        }
    
    return deliverable