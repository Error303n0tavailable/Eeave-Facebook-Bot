import requests

class TextEncoder:
    def encode_text(self, text):
        try:
            response = requests.get(f"https://api.popcat.xyz/encode?text={text}")
            if response.status_code == 200:
                json_response = response.json()
                print(f"API Response JSON: {json_response}")  # Log the full JSON response
                encoded_text = json_response.get("binary")
                if encoded_text:
                    return encoded_text
                else:
                    return "Failed to encode text: 'binary' key not found in response."
            else:
                return f"Failed to encode text: HTTP {response.status_code}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
