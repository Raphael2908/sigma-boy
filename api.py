from typing import Union
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import shutil
import os
import jawline_math as jm

app = FastAPI()
shape_list = ["Round", "Long"]

s3Helper = s3Helper.s3Helper()

# Simple File Upload logic from user (Change to fit ACP)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

@app.get("/mog")
def mog(image: str) -> str:
    return "Hello world"


@app.post("/upload")
async def upload(file: UploadFile) -> dict: 
    if not file or not file.filename: 
        return "Please send file"
        
    try: 
        s3_image_url = s3Helper.upload(file.filename, "test", "Help me")
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
    
    