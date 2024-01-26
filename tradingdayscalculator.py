import pandas as pd
import pandas_market_calendars as mcal

# Get the NSE calendar
nse = mcal.get_calendar('NSE')


'''
# input as yyyy-mm-dd
input_date = '2024-01-26'
print(get_previous_trading_date(input_date, 7))

# output
market_open    2024-01-18 03:45:00+00:00
market_close   2024-01-18 10:00:00+00:00
Name: 2024-01-18 00:00:00, dtype: datetime64[ns, UTC]
'''

def get_previous_trading_date(input_date, tradingsessions):
    # Convert the input date to a pandas Timestamp
    input_date = pd.Timestamp(input_date)

    # Get all the trading days in the last 'trading_days_behind' days
    trading_days = nse.schedule(start_date=input_date - pd.DateOffset(days=tradingsessions * 2), end_date=input_date)

    # Get the date 'trading_days_behind' days behind
    previous_trading_date = trading_days.iloc[-tradingsessions]

    return previous_trading_date


