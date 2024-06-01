import requests

def get_webgpt4o_response(question):
    try:
        api_url = f"https://hiroshi-rest-api.replit.app/ai/webgpt4o?ask={question}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"response": f"Sorry, an error occurred while processing your request. Status code: {response.status_code}"}
    except Exception as e:
        return {"response": f"An error occurred while processing your request: {str(e)}"}
