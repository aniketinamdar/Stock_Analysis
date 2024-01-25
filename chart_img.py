import requests
from datetime import datetime, timedelta

def download_image(sname="HDFCBANK", exch="NSE", inter="15m", rng_from="2024-01-20T00:00:00.000Z", rng_to="2024-01-20T15:16:00.000Z"):
    url = 'https://api.chart-img.com/v2/tradingview/advanced-chart'  # Replace with the actual URL
    save_path = 'chart_img.png'  # Replace with your desired path

    try:
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
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                return f"Image successfully saved to {save_path}"
            else:
                return "Error: The URL does not point to an image"
        else:
            return f"Error: Received response status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Example usage


# result = download_image(url, save_path)
# print(result)
