from typing import Union
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import shutil
import os
import jawline_math as jm
# Temporarily commenting out these imports for testing
# from acp import buyer
# from utils import s3Helper

app = FastAPI()
shape_list = ["Round", "Long"]

# Temporarily commented out for testing
# s3Helper = s3Helper.s3Helper()

# Simple File Upload logic from user (Change to fit ACP)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.post("/iniate-buyer")
# async def iniate_buyer(): 
#     buyer()


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # save the uploaded file to disk
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message":  f"Image saved at {file_path}"
    }

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get-image/{filename}")
def process_image(filename : str):
    uploaded_file = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(uploaded_file):
        return f'error : {filename} not found'
    
    image = Image.open(uploaded_file)
    output_image, landmarks = jm.draw_face_landmarks(image)

    if output_image is not None and landmarks:
        # placeholder (initially used to do a side-by-side comparison on st)
        print("landmarks")
        shape = jm.classify_face_shape(landmarks, image.size[::-1])
        print(f"🧬 Detected Face Shape:** `{shape}`")
        
        if shape in shape_list:
            return "⚠️ Your jawline could be enhanced with regular exercises."

        else:
            return "🎯 Your jawline appears naturally well-defined based on facial proportions!"
    else:
        return "⚠️Warning: Could not detect a face. Try another photo."


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

from gemini_evaluator.evaluator import analyze_facial_features

@app.get("/mog")
async def mog(image: str, prompt: str, job_id: str) -> dict:
    try:
        print(f"Processing request for image: {image}")
        # First process the image with your existing jawline detection
        uploaded_file = os.path.join(UPLOAD_FOLDER, image)
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
            return {"formatted_response": readable_response}
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


# Temporarily commented out for testing
# @app.post("/upload")
# async def upload(file: UploadFile) -> dict: 
#     if not file or not file.filename: 
#         return "Please send file"
        
#     try: 
#         s3_image_url = s3Helper.upload(file.filename, "test", "Help me")
#         print(s3_image_url)
#     except Exception as e:
#         print(e)
#         response_error: dict = {
#             "error": True, "error messsage": e
#         }
#         return response_error
#     else: 
#         response_successful: dict = {
#             "error": False, "image_url": s3_image_url 
#         }
#         return response_successful 
    
    