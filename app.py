import streamlit as st
from model import *

st.set_page_config(page_title="Stock Analysis")
st.header("Stock Analysis")

stock_name=st.text_area("Stock Name ",key="input",placeholder="Enter stock name")
exchange=st.selectbox(
    "Exchange",
    ("NSE","BSE"),
    index=None,
    placeholder="Select the exchnage (BSE/NSE)"
)
st.write('You Selected:', exchange)

uploaded_file=st.file_uploader("Upload the tradingview chart ",type=["jpg","png"])
# uploaded_file=st.file_uploader("Upload the tradingview chart ")
if uploaded_file is not None:
    st.write("Chart Uploaded Successfully")

time_frame=st.selectbox(
    "Time Frame",
    ("1 Year","6 Month","3 Month","1 Month","1 Week","1 Day","1 Hr","30 min","15 min","5 min","3 min","1 min"),
    index=None,
    placeholder="Select the time frame "
)
st.write('You Selected:', time_frame)

trade_setup=st.selectbox(
    "Trade Setup",
    ("Intraday","Swing","Long Term"),
    index=None,
    placeholder="Select the trade setup "
)
st.write('You Selected:', trade_setup)

submit1 = st.button("Technical Analysis")

submit2 = st.button("Fundamental Analysis")

submit3 = st.button("Give me the possible positions for the trade")

input_prompt1 = """
You are a stock market expert. I am providing you with the {tframe} chart for {stock} stock listed on {xchange}. I want a detailed technical analysis of the chart for {tsetup} trading. Please provide general information about the price trends, key technical indicators, and any notable patterns or support/resistance levels in the chart.
""".format(tframe=time_frame, stock=stock_name, xchange=exchange, tsetup=trade_setup)

input_prompt2 = """
You are a stock market expert. I am providing you with the {tframe} chart for {stock} stock listed on {xchange}. I want a detailed fundamental analysis of the stock for {tsetup} trading. Please analyze the fundamental aspects of the stock, such as earnings, revenue, and financial ratios, and provide general information about its financial health and outlook.
""".format(tframe=time_frame, stock=stock_name, xchange=exchange)

input_prompt3 = """
You are a stock market expert. I am providing you with the {tframe} chart for {stock} stock listed on {xchange}. I am looking to analyze the stock for {tsetup} trading. Please provide me with the possible entry, target, and stop-loss levels for the given stock and setup, based on your technical analysis of the chart.
""".format(tframe=time_frame, stock=stock_name, xchange=exchange, tsetup=trade_setup)


if submit1:
    if uploaded_file is not None:
        response=get_gemini_response(uploaded_file,input_prompt1)
        st.subheader("Technical Analysis ")
        st.write(response)
    else:
        st.write("Chart Not Uploaded")

elif submit2:
    if stock_name is not None and uploaded_file is not None:
        response=get_gemini_response(uploaded_file,input_prompt2)
        st.subheader("Fundamental Analysis ")
        st.write(response)
    else:
        st.write("Stock name/Chart Not Uploaded")

elif submit3:
    if stock_name is not None and uploaded_file is not None and trade_setup is not None:
        response=get_gemini_response(uploaded_file,input_prompt3)
        st.subheader("Entry/Stoploss/Target is ")
        st.write(response)
    else:
        st.write("Stock Name/Chart/Trade Setup Not Uploaded")