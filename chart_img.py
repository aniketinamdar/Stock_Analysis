import requests
import io
from datetime import datetime, timedelta

def download_image(
    sname="HDFCBANK", exch="NSE", inter="15m",
    rng_from="2024-01-20T00:00:00.000Z",
    rng_to="2024-01-20T15:16:00.000Z"
):
    try:
        url = "https://api.chart-img.com/v2/tradingview/advanced-chart"
        headers = {"x-api-key": "n9M8bbb2Pe9b3i5oNRQiZ5ADVrXzZPWh54riYxH4"}
        payload = {
            "symbol": f"{exch}:{sname}",
            "range": {
                "from": f"{rng_from}",
                "to": f"{rng_to}"
            },
            "interval": f"{inter}",
            "timezone": "Asia/Kolkata",
            "theme": "dark",
            "studies": [
                {
                    "name": "Volume",
                    "forceOverlay": True
                }
            ]
        }
        response = requests.post(url, json = payload, headers = headers)
        if response.status_code == 200:
            # Check if the response is an image
            if 'image' in response.headers['Content-Type']:
                # with open(save_path, 'wb') as file:
                #     file.write(response.content)
                # return f"Image successfully saved to {save_path}"
                print("response type", type(response.content))
                return io.BytesIO(response.content)
            else:
                print(response.content)
                return None
        else:
            print(response.status_code, response.content)
            return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None

# Example usage


# result = download_image(url, save_path)
# print(result)
