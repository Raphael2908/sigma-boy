# 🗿 Sigma-Boi: The Ultimate Facial Analysis Tool

A humorous yet functional facial analysis tool that combines MediaPipe facial landmark detection with Google's Gemini Vision API to provide "sigma male" style facial feature analysis and improvement suggestions.

## 🚀 Features

- Facial landmark detection using MediaPipe
- Advanced jawline shape analysis
- Full facial feature analysis using Gemini Vision AI
- Meme-worthy "sigma male" style improvement suggestions
- Easy-to-use API endpoints
- CLI testing interface

## 📋 Prerequisites

- Python 3.8+
- A Google API key (for Gemini Vision API)
- Virtual environment (recommended)

## ⚙️ Setup

1. Clone the repository:
```bash
git clone https://github.com/Raphael2908/sigma-boi.git
cd sigma-boi
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create required directories:
```bash
mkdir uploads guidance mesh evaluation templates
```

5. Set up environment variables:
Create a `.env` file in the project root with:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
# or
GEMINI_API_KEY=your_gemini_api_key_here
```

6. Set up AWS credentials (for S3 storage):
```env
# Add to your .env file:
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

## 🏃‍♂️ Running the Application

1. Start the FastAPI server:
```bash
fastapi dev
```

2. Start sigma-boi: 
```bash
python acp/sigma-boy.py
```

3. Start buyer: 
```bash
python acp/buyer.py
```
4. View results: 

> got to: https://app.virtuals.io/acp

> search: "sigma boi"

> select job and view result


## 📝 API Endpoints

### 1. Upload Image
- **Endpoint**: `/upload-image/`
- **Method**: POST
- **Input**: Form data with image file
- **Returns**: Upload confirmation with file path

### 2. Analyze Face (MOG)
- **Endpoint**: `/mog`
- **Method**: GET
- **Parameters**:
  - `image`: filename of uploaded image
  - `prompt`: analysis prompt
  - `unique_key`: unique identifier
- **Returns**: Comprehensive facial analysis including:
  - Jawline assessment
  - Mewing techniques
  - Sigma grindset tips
  - Feature-by-feature analysis
  - Improvement suggestions

## 🎯 Example Usage

1. Upload an image:
```python
import requests

with open('your_image.png', 'rb') as img:
    files = {'file': ('image.png', img, 'image/png')}
    response = requests.post('http://127.0.0.1:8000/upload-image/', files=files)
```

2. Get analysis:
```python
params = {
    'image': 'image.png',
    'prompt': 'Analyze my facial features',
    'unique_key': 'test1'
}
analysis = requests.get('http://127.0.0.1:8000/mog', params=params)
print(analysis.json()['formatted_response'])
```

## 🏗️ Project Structure

```
sigma-boi/
├── api.py              # FastAPI server and endpoints
├── jawline_math.py     # Jawline detection logic
├── gemini_evaluator/   # Gemini Vision integration
│   └── evaluator.py    # Feature analysis logic
├── services/           # Business logic services
│   ├── jawline_service.py    # MediaPipe jawline analysis
│   ├── gemini_service.py     # AI facial feature analysis
│   └── file_service.py       # File upload/download management
├── formatters/         # Response formatting
│   └── response_formatter.py # Sigma male report formatting
├── utils/              # Utility functions
│   └── s3Helper.py     # AWS S3 integration
├── test_cli.py        # CLI testing interface
├── requirements.txt    # Project dependencies
├── uploads/           # Uploaded images directory (create locally)
├── guidance/          # Generated analysis files (create locally)
├── mesh/              # Processed images with landmarks (create locally)
├── evaluation/        # Downloaded S3 files cache (create locally)
└── templates/         # HTML templates (create locally)
```

> **Note**: Directories marked with "(create locally)" are ignored by git but required for the application to run. Use the setup command above to create them.

## 🛠️ Development

- The project uses FastAPI for the backend
- MediaPipe for facial landmark detection
- Google's Gemini Vision API for advanced feature analysis
- Async/await patterns for efficient API handling

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MediaPipe for facial landmark detection
- Google's Gemini Vision API for advanced analysis
- The sigma male community for inspiration 🗿
