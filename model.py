from dotenv import load_dotenv

load_dotenv()

import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#updated prompts to come here

def get_fundamental_prompt(time_frame, stock_name, exchange, trade_setup):
    input_prompt2 = """
    You are a stock market expert. I am providing you with the {tframe} chart for {stock} stock listed on {xchange}. I want a detailed fundamental analysis of the chart for {tsetup}. Please analyze the fundamental aspects of the stock, such as earnings, revenue, and financial ratios, and provide general information about its financial health and outlook.
    """.format(tframe=time_frame, stock=stock_name, xchange=exchange,  tsetup=trade_setup)
    
    return input_prompt2

def get_technical_prompt(time_frame, stock_name, exchange, trade_setup):
    input_prompt1 = """
    You are a stock market expert. I am providing you with the {tframe} chart for {stock} stock listed on {xchange}. I want a detailed technical analysis of the chart for {tsetup} trading.. Please provide general information about the price trends, key technical indicators, and any notable patterns or support/resistance levels in the chart.
    """.format(tframe=time_frame, stock=stock_name, xchange=exchange,  tsetup=trade_setup)
    
    return input_prompt1

def get_positions(time_frame, stock_name, exchange, trade_setup):
    input_prompt3 = """
    You are a stock market expert. I am providing you with the {tframe} chart for {stock} stock listed on {xchange}. I am looking to analyze the stock for {tsetup} trading. Please provide me with the possible entry, target, and stop-loss levels for the given stock and setup, based on your technical analysis of the chart.
    """.format(tframe=time_frame, stock=stock_name, xchange=exchange, tsetup=trade_setup)

    return input_prompt3

def get_gemini_response(uploaded_file,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    file_contents = uploaded_file.read()
    image = Image.open(io.BytesIO(file_contents))
    response = model.generate_content([image,prompt])
    return response.text

