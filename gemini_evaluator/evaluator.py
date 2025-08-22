"""
Facial Features Analysis using Gemini Vision — Clean MWE
"""

import os
import json
import re
from typing import Any, Dict, List

from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# 1) Load .env from CURRENT directory (adjust if yours is elsewhere)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Set GEMINI_API_KEY or GOOGLE_API_KEY in your environment or .env")
genai.configure(api_key=api_key)

# 2) Pick one modern, vision-capable model. (gemini-2.0-flash supports images)
MODEL_NAME = "gemini-2.0-flash"  # or "gemini-1.5-flash" if you prefer

VISION_PROMPT_TEMPLATE = """
You are a sigma male facial aesthetics coach who gives intentionally over-the-top, meme-worthy advice. Your style combines internet culture, sigma male grindset, and gigachad references. Make suggestions funny but keep them somewhat grounded in real techniques. Return ONLY valid JSON, no extra text.

Schema:
{
  "jawline_enhancement": {
    "current_definition": "Sigma male analysis of jawline potential",
    "definition_score": 1-10,
    "mewing_tips": ["Over-the-top mewing advice 1", "Over-the-top mewing advice 2"],
    "sigma_grindset": ["Funny sigma male lifestyle tip 1", "Funny sigma male lifestyle tip 2"],
    "gigachad_quotes": ["Motivational quote 1", "Motivational quote 2"]
  },
  "eyes_and_eyebrows": {
    "description": "Meme-worthy analysis of eye area",
    "sigma_score": 1-10,
    "suggestions": ["Funny eye area improvement tip 1", "Funny eye area improvement tip 2"]
  },
  "nose_structure": {
    "description": "Chad-like analysis of nose features",
    "mog_score": 1-10,
    "suggestions": ["Funny nose improvement tip 1", "Funny nose improvement tip 2"]
  },
  "cheekbones": {
    "description": "Gigachad analysis of bone structure",
    "bone_score": 1-10,
    "suggestions": ["Funny bone structure tip 1", "Funny bone structure tip 2"]
  },
  "skin_quality": {
    "description": "Based analysis of skin condition",
    "zyzz_score": 1-10,
    "care_recommendations": ["Funny skincare tip 1", "Funny skincare tip 2"]
  },
  "facial_harmony": {
    "balance_description": "Overall sigma potential analysis",
    "mogger_score": 1-10,
    "enhancement_suggestions": ["Funny overall improvement tip 1", "Funny overall improvement tip 2"]
  }
}
"""

def _extract_json(text: str) -> Dict[str, Any]:
    """Try to parse JSON directly; if that fails, extract the largest JSON block."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Find the first {...} block
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass

    # Give up, but return raw text for debugging
    return {"raw_analysis": text, "note": "Response was not valid JSON"}

def analyze_facial_features(image_path: str) -> Dict[str, Any]:
    # Ensure the file exists and is an image
    Image.open(image_path).verify()  # quick sanity check (raises if invalid)

    # Upload the image to Gemini
    print(f"Uploading image: {image_path}")
    file_obj = genai.upload_file(image_path)  # returns a File handle
    print("Image uploaded successfully")

    print("Creating Gemini model...")
    model = genai.GenerativeModel(MODEL_NAME)
    print("Sending request to Gemini...")
    resp = model.generate_content([VISION_PROMPT_TEMPLATE, file_obj])
    print("Raw response from Gemini:", resp)

    # Prefer .text; fall back to assembling from candidates if needed
    print("Getting response text...")
    text = getattr(resp, "text", None)
    print("Direct text attribute:", text)
    
    if not text and getattr(resp, "candidates", None):
        print("No direct text, checking candidates...")
        parts: List[str] = []
        for c in resp.candidates:
            print("Candidate:", c)
            for p in getattr(c.content, "parts", []) or []:
                if hasattr(p, "text"):
                    print("Found text part:", p.text)
                    parts.append(p.text)
        text = "\n".join(parts).strip()
        print("Assembled text from parts:", text)

    if not text:
        return {
            "error": "No analysis generated",
            "details": "Model returned no text. Check model name and image input."
        }

    return _extract_json(text)

if __name__ == "__main__":
    # Example usage
    img_path = "face.jpg"  # change to your file
    try:
        result = analyze_facial_features(img_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
