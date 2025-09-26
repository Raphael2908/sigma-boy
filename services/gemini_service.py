"""
Gemini Analysis Service
Handles AI-powered facial feature analysis using Gemini Vision API.
"""

from gemini_evaluator.evaluator import analyze_facial_features
from typing import Dict, Any


def analyze_facial_features_service(image_path: str) -> Dict[str, Any]:
    """
    Perform AI analysis of facial features using Gemini Vision API.
    
    Args:
        image_path: Path to the image file to analyze
        
    Returns:
        Dictionary containing comprehensive facial feature analysis
        
    Raises:
        Exception: If Gemini analysis fails
    """
    print("Getting Gemini analysis...")
    
    try:
        other_features = analyze_facial_features(image_path)
        
        # Validate that we got the expected structure
        if not isinstance(other_features, dict):
            raise Exception("Invalid analysis format from Gemini")
            
        required_keys = [
            'jawline_enhancement',
            'eyes_and_eyebrows', 
            'nose_structure',
            'cheekbones',
            'skin_quality',
            'facial_harmony'
        ]
        
        for key in required_keys:
            if key not in other_features:
                raise Exception(f"Missing required analysis section: {key}")
        
        print("Gemini analysis completed successfully")
        return other_features
        
    except Exception as e:
        print(f"Error in Gemini analysis: {str(e)}")
        raise Exception(f"Failed to analyze facial features: {str(e)}")