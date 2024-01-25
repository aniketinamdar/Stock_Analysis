from dotenv import load_dotenv

load_dotenv()

import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_fundamental_prompt(time_frame, stock_name, exchange, trade_setup):
# 	input_prompt2 = """
#     You are a stock market expert. I am providing you with the {tframe} chart for {stock} stock listed on {xchange}. I want a detailed fundamental analysis of the chart for {tsetup}. Please analyze the fundamental aspects of the stock, such as earnings, revenue, and financial ratios, and provide general information about its financial health and outlook.
#     """.format(tframe=time_frame, stock=stock_name, xchange=exchange, tsetup=trade_setup)
#
# 	return input_prompt2


def get_technical_prompt(time_frame, stock_name, exchange):
	technical_prompt = f"Act as a stock market expert and perform technical analysis on the company {stock_name} listed on {exchange}. Use the {time_frame} candlestick chart provided below for the analysis. Perform an in-depth technical analysis focusing on single and multiple candlestick patterns, volume, and support - resistance levels. Return the analysis in 3 paragraphs of 80-100 words each."

	return technical_prompt

def get_intraday_prompt(stock_name, exchange):
	intraday_prompt = f"Act as a stock market expert and perform technical analysis on the company {stock_name} listed on {exchange}. Use the 5 minute and 15 minute candlestick charts provided below for the analysis. Perform an in-depth technical analysis focusing on single and multiple candlestick patterns, volume, and support - resistance levels. Using the analysis, decide whether to take long position or a short position as an intraday trader. For the chosen position, return entry price, stop-loss, target 1 and target 2. While calculating the position, keep the minimum risk reward ratio (risk reward ratio = potential loss / potential profit) above 1. If no suitable position can be found above minimum risk reward ratio, convey the same to the user."

	return intraday_prompt

def get_swing_prompt(stock_name, exchange):
	swing_prompt = f"Act as a stock market expert and perform technical analysis on the company {stock_name} listed on {exchange}. Use the 1 day and 1 week candlestick charts provided below for the analysis. Perform an in-depth technical analysis focusing on single and multiple candlestick patterns, volume, and support - resistance levels. Using the analysis, decide whether to take a long position or a short position as a swing trader. For the chosen position, return entry price, stop-loss, target 1 and target 2. While calculating the position, keep the minimum risk reward ratio (risk reward ratio = potential loss / potential profit) above 1. If no suitable position can be found above minimum risk reward ratio, convey the same to the user."

	return swing_prompt

#gemini response function to be edited
def get_gemini_response(uploaded_file, prompt):
	model = genai.GenerativeModel('gemini-pro-vision')
	file_contents = uploaded_file.read()
	image = Image.open(io.BytesIO(file_contents))
	response = model.generate_content([image, prompt])
	return response.text
