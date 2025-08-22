from typing import Union, Annotated
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from PIL import Image
import shutil
import os
import jawline_math as jm
# Temporarily commenting out these imports for testing
# from acp import buyer
from utils import s3Helper

from gemini_evaluator.evaluator import analyze_facial_features

app = FastAPI()
shape_list = ["Round", "Long"]

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
    
    # Download text
    guidance_path = f"guidance-{key}.txt"
    evaluation_path_text = f"evaluation/{guidance_path}.txt"
    
    s3Helper.download(guidance_path, evaluation_path_text)

    with open(evaluation_path_text, 'r') as file:
        content = file.read()

    templates = Jinja2Templates(directory="templates")

    DOCS_DIR = Path("evaluation").resolve()  # put your .txt files here

    path = (DOCS_DIR /f"{guidance_path}.txt").resolve()
    guidance = path.read_text(encoding="utf-8")
    

        
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


@app.get("/mog")
async def mog(image: str, prompt: str, unique_key: str) -> dict:
    try:
        print(f"Processing request for image: {image}")
        # First process the image with your existing jawline detection
        uploaded_file = s3Helper.download(unique_key, f"{UPLOAD_FOLDER}/{unique_key}.png")
        if not os.path.exists(uploaded_file):
            print(f"Image not found: {uploaded_file}")
            return {"error": f"Image {image} not found"}
        
        print("Processing image with jawline detection...")
        # Process image with existing jawline detection
        img = Image.open(uploaded_file)
        output_image, landmarks = jm.draw_face_landmarks(img)
        
        if output_image is not None and landmarks:
            print("Landmarks detected, analyzing jawline...")
            # Get jawline analysis from your existing code
            jawline_shape = jm.classify_face_shape(landmarks, img.size[::-1])
            jawline_assessment = (
                "⚠️ Your jawline could be enhanced with regular exercises."
                if jawline_shape in shape_list
                else "🎯 Your jawline appears naturally well-defined based on facial proportions!"
            )
            
            print("Getting Gemini analysis...")
            # Get Gemini's analysis for other facial features
            other_features = analyze_facial_features(uploaded_file)
            
            # Format the response in a readable way
            readable_response = f"""� SIGMA MALE FACIAL ANALYSIS REPORT 💪

🗿 JAWLINE ASSESSMENT (MOST IMPORTANT):
• Current Shape: {jawline_shape}
• Basic Assessment: {jawline_assessment}
• Sigma Analysis: {other_features['jawline_enhancement']['current_definition']}
• Mogger Score: {other_features['jawline_enhancement']['definition_score']}/10

� ADVANCED MEWING TECHNIQUES:
  - {other_features['jawline_enhancement']['mewing_tips'][0]}
  - {other_features['jawline_enhancement']['mewing_tips'][1]}

🔱 SIGMA GRINDSET TIPS:
  - {other_features['jawline_enhancement']['sigma_grindset'][0]}
  - {other_features['jawline_enhancement']['sigma_grindset'][1]}

💎 GIGACHAD WISDOM:
  "{other_features['jawline_enhancement']['gigachad_quotes'][0]}"
  "{other_features['jawline_enhancement']['gigachad_quotes'][1]}"

👁️ HUNTER EYES ANALYSIS:
• Analysis: {other_features['eyes_and_eyebrows']['description']}
• Sigma Score: {other_features['eyes_and_eyebrows']['sigma_score']}/10
• How to Mog:
  - {other_features['eyes_and_eyebrows']['suggestions'][0]}
  - {other_features['eyes_and_eyebrows']['suggestions'][1]}

👃 NOSE ASSESSMENT:
• Chad Analysis: {other_features['nose_structure']['description']}
• Mog Score: {other_features['nose_structure']['mog_score']}/10
• Ascension Tips:
  - {other_features['nose_structure']['suggestions'][0]}
  - {other_features['nose_structure']['suggestions'][1]}

💀 BONE STRUCTURE:
• Gigachad Analysis: {other_features['cheekbones']['description']}
• Bone Score: {other_features['cheekbones']['bone_score']}/10
• How to Ascend:
  - {other_features['cheekbones']['suggestions'][0]}
  - {other_features['cheekbones']['suggestions'][1]}

✨ SKIN MAXING:
• Based Analysis: {other_features['skin_quality']['description']}
• Zyzz Score: {other_features['skin_quality']['zyzz_score']}/10
• Skinmaxxing Tips:
  - {other_features['skin_quality']['care_recommendations'][0]}
  - {other_features['skin_quality']['care_recommendations'][1]}

👑 OVERALL MOGGER POTENTIAL:
• Sigma Analysis: {other_features['facial_harmony']['balance_description']}
• Mogger Score: {other_features['facial_harmony']['mogger_score']}/10
• How to Become Gigachad:
  - {other_features['facial_harmony']['enhancement_suggestions'][0]}
  - {other_features['facial_harmony']['enhancement_suggestions'][1]}"""
            
            print("Analysis complete!")
            mesh_image = Image.fromarray(output_image)
            mesh_path = f"mesh/{unique_key}.png"
            mesh_image.save(mesh_path)
            mesh_key = f"mesh-{unique_key}"
            mesh_url = s3Helper.upload(image_path=mesh_path, key=mesh_key)

            # Save text
            guidance_path = f"guidance/guidance-{unique_key}.txt"
            with open(guidance_path, "w") as file:
              file.write(readable_response)
            
            s3Helper.upload_txt(filename=guidance_path, unique_key=unique_key) 
            return {"formatted_response": readable_response, "mesh_key": mesh_key}
        else:
            print("No landmarks detected")
            return {
                "error": "Could not detect face landmarks",
                "landmarks_detected": False
            }
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
        s3_image_url = s3Helper.upload(image.filename, key, prompt)
        print(s3_image_url)
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

