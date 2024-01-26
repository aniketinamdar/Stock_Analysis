from dotenv import load_dotenv

load_dotenv()

import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_fundamental_prompt(stock_name, exchange):
	fundamental_prompt = f"Act as a stock market expert and perform fundamental analysis on the company {stock_name} listed on {exchange}. Assess the company's financial health by analyzing its most recent balance sheet, income statement, and cash flow statement. Evaluate its management effectiveness, competitive position in the industry, and future growth prospects. Provide insights into the company's valuation metrics like P/E ratio, P/B ratio, EPS, dividend yield, market cap, and shares float. Return the analysis in four paragraphs, each containing 80-100 words, language: english."
	return fundamental_prompt

def get_technical_prompt(time_frame, stock_name, exchange):
	technical_prompt = f"Act as a stock market expert and perform technical analysis on the company {stock_name} listed on {exchange}. Use the {time_frame} candlestick chart provided below for the analysis. Perform an in-depth technical analysis focusing on single and multiple candlestick patterns, volume, and support - resistance levels. Output format should be as follows: 3 paragraphs of 80-100 words each, language: english."
	return technical_prompt

def get_intraday_prompt(stock_name, exchange):
	intraday_prompt = f"Act as a stock market expert and perform technical analysis on the company {stock_name} listed on {exchange}. Use the 5 minute and 15 minute candlestick charts provided below for the analysis. Perform an in-depth technical analysis focusing on single and multiple candlestick patterns, volume, and support - resistance levels. Using the analysis, decide whether to take long position or a short position as an intraday trader. While calculating the position, keep the minimum risk reward ratio (risk reward ratio = potential loss / potential profit) above 1. Output format should be as follows: Position- long or short, Entry price: in rs, Stop loss: in rs, Target 1: in rs, Target 2: in rs with language: english. If no suitable position can be found above minimum risk reward ratio, convey the same to the user."
	return intraday_prompt

def get_swing_prompt(stock_name, exchange):
	swing_prompt = f"Act as a stock market expert and perform technical analysis on the company {stock_name} listed on {exchange}. Use the 1 day and 1 week candlestick charts provided below for the analysis. Perform an in-depth technical analysis focusing on single and multiple candlestick patterns, volume, and support - resistance levels. Using the analysis, decide whether to take long position or a short position as an intraday trader. While calculating the position, keep the minimum risk reward ratio (risk reward ratio = potential loss / potential profit) above 1. Output format should be as follows: Position- long or short, Entry price: in rs, Stop loss: in rs, Target 1: in rs, Target 2: in rs with language: english. If no suitable position can be found above minimum risk reward ratio, convey the same to the user."
	return swing_prompt


# use this function for technical analysis
def get_gemini_ta_response(user_uploaded_chart, prompt):
	model = genai.GenerativeModel('gemini-pro-vision')
	file_contents = user_uploaded_chart.read()
	image = Image.open(io.BytesIO(file_contents))
	response = model.generate_content([image, prompt])
	return response.text

# use this function for intraday or swing
def get_gemini_intraday_or_swing_response(api_file_1, api_file_2, prompt):
	model = genai.GenerativeModel('gemini-pro-vision')
	file_contents_1 = api_file_1.read()
	image_1 = Image.open(io.BytesIO(file_contents_1))
	file_contents_2 = api_file_2.read()
	image_2 = Image.open(io.BytesIO(file_contents_2))
	response = model.generate_content([image_1, image_2, prompt])
	return response.text

def get_positions_gemini(img_byte_obj1, img_byte_obj2, prompt):
	model = genai.GenerativeModel('gemini-pro-vision')
	image_1 = Image.open(img_byte_obj1)
	image_2 = Image.open(img_byte_obj2)
	response = model.generate_content([image_1, image_2, prompt])
	return response.text
