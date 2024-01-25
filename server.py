from flask import Flask, jsonify, request

from chart_img import *
from model import *
import pytz

app = Flask(__name__)


def get_curr_time(tmz="Asia/Kolkata"):
    return datetime.now(pytz.timezone(tmz))

def get_range_formatted(del_time_dec, del_time_inc):
    curr_time = get_curr_time()
    from_time = curr_time - del_time_dec
    to_time = curr_time + del_time_inc
    return (from_time.strftime("%y-%m-%dT%H:%M:%S.%fZ"), to_time.strftime("%y-%m-%dT%H:%M:%S.%fZ"))

def get_range_years():
    return get_range_formatted(timedelta(days=365*3), timedelta(days=180))

def get_range_months():
    pass

def get_range_days():
    return get_range_formatted(timedelta(days=3), timedelta(days=1))


# Define an endpoint for the root URL
@app.route('/')
def home():
    return 'Welcome to the Flask App!'

# Define an endpoint for /hello
@app.route('/test', methods=['GET'])
def test():
    print(request.args)
    stock_name = request.args.get('stk')
    exchange = request.args.get('exc')
    interval = request.args.get('int')
    trade_type = request.args.get('trd')
    prompt_type = request.args.get('pmt')
    from_time, to_time = (
        get_range_days() if trade_type == "intra" else
        get_range_years() if trade_type == "swing" else
        (None, None)
    )
    print(stock_name, exchange, interval, trade_type, )
    download_image(sname=stock_name, exch=exchange, inter=interval, rng_from=from_time, rng_to=to_time)
    print("image downloaded")
    prompt = (
        get_fundamental_prompt() if prompt_type == "fundamental" else
        get_technical_prompt() if prompt_type == "technical" else
        get_positions()
    )
    resp = None
    with open("chart_img.png", "rb") as file:
        resp = get_gemini_response(file, prompt)
    print("gemini response:", resp)
    # call model and return that shit
    return resp


if __name__ == '__main__':
    app.run(debug=True, port=4000)
