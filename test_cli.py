import requests
from PIL import Image
import io
import os

def test_jawline():
    # Print current directory and check if files exist
    print("Current directory:", os.getcwd())
    print("Files in current directory:", os.listdir())
    
    # 1. Upload image
    image_path = "SleepyJoe.png"  # or "Caleb.png"
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found!")
        return
    
    print(f"Found image file: {image_path}")
    
    try:
        # 1. Upload image
        with open(image_path, 'rb') as img:
            files = {'file': (image_path, img, 'image/png')}
            print("Uploading image...")
            upload_response = requests.post('http://127.0.0.1:8000/upload-image/', files=files)
            print("Upload response:", upload_response.text)
            print("Upload status code:", upload_response.status_code)

        # 2. Get analysis
        print("\nGetting analysis...")
        analysis_params = {
            'image': image_path,
            'prompt': 'Analyze my facial features',
            'job_id': 'test1'
        }
        analysis_response = requests.get('http://127.0.0.1:8000/mog', params=analysis_params)
        print("Analysis status code:", analysis_response.status_code)
        response_data = analysis_response.json()
        if "formatted_response" in response_data:
            # Clean up any potential duplicate newlines
            clean_response = "\n".join(line for line in response_data["formatted_response"].splitlines() if line.strip())
            print("\n" + clean_response)
        else:
            print("Analysis response:", analysis_response.text)
        
    except Exception as e:
        print("Error occurred:", str(e))

if __name__ == "__main__":
    test_jawline()
