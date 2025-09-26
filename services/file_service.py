"""
File Management Service
Handles saving images and text files locally and uploading to S3.
"""

import os
from PIL import Image
import numpy as np
from utils import s3Helper

# Initialize S3 helper
s3_helper = s3Helper.s3Helper()


def save_and_upload_mesh_image(output_image: np.ndarray, unique_key: str) -> tuple[str, str]:
    """
    Save mesh image locally and upload to S3.
    
    Args:
        output_image: NumPy array containing the processed image with landmarks
        unique_key: Unique identifier for the file
        
    Returns:
        Tuple of (mesh_key, mesh_url) - S3 key and presigned URL
    """
    # Ensure mesh directory exists
    os.makedirs("mesh", exist_ok=True)
    
    # Save mesh image locally
    mesh_image = Image.fromarray(output_image)
    mesh_path = f"mesh/{unique_key}.png"
    mesh_image.save(mesh_path)
    
    # Upload to S3
    mesh_key = f"mesh-{unique_key}"
    mesh_url = s3_helper.upload(image_path=mesh_path, key=mesh_key)
    
    return mesh_key, mesh_url


def save_and_upload_analysis_text(analysis_text: str, unique_key: str) -> str:
    """
    Save analysis text locally and upload to S3.
    
    Args:
        analysis_text: The formatted analysis report text
        unique_key: Unique identifier for the file
        
    Returns:
        Local file path where the text was saved
    """
    # Ensure guidance directory exists
    os.makedirs("guidance", exist_ok=True)
    
    # Save analysis text locally
    guidance_path = f"guidance/guidance-{unique_key}.txt"
    with open(guidance_path, "w") as file:
        file.write(analysis_text)
    
    # Upload to S3
    s3_helper.upload_txt(filename=guidance_path, unique_key=unique_key)
    
    return guidance_path