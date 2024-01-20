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

# def input_pdf_setup(uploaded_file):
#     if uploaded_file is not None:
#         images=pdf2image.convert_from_bytes(uploaded_file.read())
#         first_page = images[0]
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr,format='JPEG')
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_parts = [
#             {
#                 "mime_type": "image/jpeg",
#                 "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
#             }
#         ]
#         return pdf_parts
#     else:
#         raise FileNotFoundError("No file uploaded")