from dotenv import load_dotenv

load_dotenv()

import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(uploaded_file,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    file_contents = uploaded_file.read()
    image = Image.open(io.BytesIO(file_contents))
    response = model.generate_content([image,prompt])
    return response.text

