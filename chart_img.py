import requests

def download_image(url, save_path):
    try:
        headers = {"x-api-key": "n9M8bbb2Pe9b3i5oNRQiZ5ADVrXzZPWh54riYxH4"}
        payload = {
            "symbol": "NSE:HDFCBANK",
            "range": {
                "from": "2024-01-20T00:00:00.000Z",
                "to": "2024-01-20T15:16:00.000Z"
            },
            "interval": "15m",
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
url = 'https://api.chart-img.com/v2/tradingview/advanced-chart'  # Replace with the actual URL
save_path = 'char_img.png'  # Replace with your desired path

result = download_image(url, save_path)
print(result)
