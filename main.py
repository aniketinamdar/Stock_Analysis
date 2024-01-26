from flask import Flask, jsonify, request
from flask_cors import CORS

from chart_img import *
from model import *
from fundamental_scraper import *
import pytz

app = Flask(__name__)

CORS(app)


def get_curr_time(tmz="Asia/Kolkata"):
  return datetime.now(pytz.timezone(tmz))


def get_range_formatted(del_time_dec, del_time_inc):
  curr_time = get_curr_time()
  from_time = curr_time - del_time_dec
  to_time = curr_time + del_time_inc
  return (from_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
          to_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))


def get_range_years(inc, dec):
  return get_range_formatted(timedelta(days=inc), timedelta(days=dec))


def get_range_months():
  pass


def get_range_days(inc, dec):
  return get_range_formatted(timedelta(days=inc), timedelta(days=dec))


prompt_type_values = {
    "intra": {
        "from_to_func": get_range_days,
        "from": (7, 35),
        "to": (1, 1),
        "intervals": ("5m", "15m"),
        "prompt": get_intraday_prompt
    },
    "swing": {
        "from_to_func": get_range_years,
        "from": (150, 700),
        "to": (10, 50),
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


@app.route('/fundamental', methods=['GET'])
def get_fundamental():
  print(request.args)
  stock_name = request.args.get('stk')
  exchange = request.args.get('exc')
  scraper_data, prompt_data = fundamental_scraper(stock_name)
  prompt = get_fundamental_prompt(stock_name, exchange, prompt_data)
  resp = get_gemini_fundamental_response(prompt)
  return scraper_data + "\n\n" + resp


@app.route('/technical', methods=['POST'])
def get_technical():
  print(request.args)
  stock_name = request.args.get('stk')
  exchange = request.args.get('exc')
  time_frame = request.args.get('tmf')
  print("request params", stock_name, exchange, time_frame)
  print(request.files)
  if "chartImage" in request.files:
    img = request.files["chartImage"]
    print(type(img))
    prompt = get_technical_prompt(time_frame, stock_name, exchange)
    resp = get_gemini_ta_response(img, prompt)
    print("gemini response:", resp)
    return resp
  else:
    return "image not uploaded", 400


@app.route('/positions', methods=['GET'])
def get_positions():
  stock_name = request.args.get('stk')
  exchange = request.args.get('exc')
  prompt_type = request.args.get('pmt')
  print("request params", stock_name, exchange, prompt_type)

  prompt_type_value = prompt_type_values.get(prompt_type, default_values)
  interval1, interval2 = prompt_type_value["intervals"]

  from_time, to_time = prompt_type_value["from_to_func"](
      prompt_type_value["from"][0], prompt_type_value["to"][0])
  img_byte_obj1 = download_image(sname=stock_name,
                                 exch=exchange,
                                 inter=interval1,
                                 rng_from=from_time,
                                 rng_to=to_time,
                                 save_path="chart_img1.png")
  from_time, to_time = prompt_type_value["from_to_func"](
      prompt_type_value["from"][1], prompt_type_value["to"][1])
  img_byte_obj2 = download_image(sname=stock_name,
                                 exch=exchange,
                                 inter=interval2,
                                 rng_from=from_time,
                                 rng_to=to_time,
                                 save_path="chart_img2.png")
  if img_byte_obj1 is None or img_byte_obj2 is None:
    return "error", 500
  print("image downloaded")

  prompt = prompt_type_value["prompt"](stock_name, exchange)
  print("calcualted params", from_time, to_time, interval1, interval2)
  print("prompt", prompt)

  resp = get_positions_gemini(img_byte_obj1, img_byte_obj2, prompt)
  print("gemini response:", resp)

  return resp


if __name__ == "__main__":
  from waitress import serve
  serve(app, host="0.0.0.0", port=8080)
