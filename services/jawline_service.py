"""
Jawline Analysis Service
Handles MediaPipe face landmark detection and jawline classification.
"""

from PIL import Image
import jawline_math as jm
import numpy as np

# TODO: This should be imported from jawline_math or defined properly
shape_list = ["round", "square", "heart", "oval"]  # Add your actual shape list here


class JawlineAnalysisResult:
    """Data class for jawline analysis results"""
    def __init__(self, jawline_shape: str, jawline_assessment: str, output_image: np.ndarray, landmarks):
        self.jawline_shape = jawline_shape
        self.jawline_assessment = jawline_assessment
        self.output_image = output_image
        self.landmarks = landmarks


def analyze_jawline(image_path: str) -> JawlineAnalysisResult:
    """
    Perform complete jawline analysis on an image.
    
    Args:
        image_path: Path to the image file to analyze
        
    Returns:
        JawlineAnalysisResult containing shape, assessment, processed image, and landmarks
        
    Raises:
        Exception: If no face landmarks are detected
    """
    print("Processing image with jawline detection...")
    
    # Load and process image with MediaPipe
    img = Image.open(image_path)
    output_image, landmarks = jm.draw_face_landmarks(img)
    
    if output_image is None or landmarks is None:
        raise Exception("Could not detect face landmarks")
    
    print("Landmarks detected, analyzing jawline...")
    
    # Classify face shape
    jawline_shape = jm.classify_face_shape(landmarks, img.size[::-1])
    
    # Generate assessment
    jawline_assessment = (
        "Your jawline could be enhanced with regular exercises."
        if jawline_shape in shape_list
        else "Your jawline appears naturally well-defined based on facial proportions!"
    )
    
    return JawlineAnalysisResult(
        jawline_shape=jawline_shape,
        jawline_assessment=jawline_assessment,
        output_image=output_image,
        landmarks=landmarks
    )