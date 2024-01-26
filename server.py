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
    return (from_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), to_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

def get_range_years():
    return get_range_formatted(timedelta(days=365), timedelta(days=100))

def get_range_months():
    pass

def get_range_days():
    return get_range_formatted(timedelta(days=7), timedelta(days=1))



prompt_type_values = {
    "intra": {
        "from_to": get_range_days(),
        "intervals": ("5m", "15m"),
        "prompt": get_intraday_prompt
    },
    "swing": {
        "from_to": get_range_years(),
        "intervals": ("1D", "1W"),
        "prompt": get_swing_prompt
    }
}

default_values = {
    "from_to": (None, None),
    "intervals": (None, None),
    "prompt": None
}



# Define an endpoint for the root URL
@app.route('/')
def home():
    return 'Backend server running'


@app.route('/analysis', methods=['GET'])
def get_analysis():
    print(request.args)
    return 'work in progress'


@app.route('/positions', methods=['GET'])
def get_positions():
    print(request.args)
    stock_name = request.args.get('stk')
    exchange = request.args.get('exc')
    prompt_type = request.args.get('pmt')
    print("request params", stock_name, exchange, prompt_type)

    prompt_type_value = prompt_type_values.get(prompt_type, default_values)
    from_time, to_time = prompt_type_value["from_to"]
    interval1, interval2 = prompt_type_value["intervals"]
    prompt = prompt_type_value["prompt"](stock_name, exchange)
    print("calcualted params", from_time, to_time, interval1, interval2)
    print("prompt", prompt)

    img_byte_obj1 = download_image(sname=stock_name, exch=exchange, inter=interval1, rng_from=from_time, rng_to=to_time)
    img_byte_obj2 = download_image(sname=stock_name, exch=exchange, inter=interval2, rng_from=from_time, rng_to=to_time)
    if (img_byte_obj1 == None or img_byte_obj2 == None):
        return "error"
    print("image downloaded")

    resp = get_positions_gemini(img_byte_obj1, img_byte_obj2, prompt)
    print("gemini response:", resp)

    return resp


if __name__ == '__main__':
    app.run(debug=True, port=4000)
