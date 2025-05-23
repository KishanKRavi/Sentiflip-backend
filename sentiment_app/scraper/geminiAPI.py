from google import genai
import json
import os
from dotenv import load_dotenv
# Load environment variables from .env
load_dotenv()
# Access the Gemini API Key from the environment
key = os.getenv("GEMINI_API_KEY")
# Your Gemini API Key
client = genai.Client(api_key=key)
data = []
# Get response from Gemini API
def gemeniAPI(query):
    pre = "Provide a **detailed review** of the **"
    ins = query # Get the first product title from the JSON file
    post = """
            **  in JSON format. 
            Include the following fields:
            {
                "product_name": ,
                "features": [],
                "pros": [],
                "cons": [],
                "summary": ,
                "bestFor": ,
                }
            """
    newQuery = pre + ins + post
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=newQuery
    )
    # Extract text content from the response
    text_response = response.candidates[0].content.parts[0].text
    json_text = text_response.strip("```json\n").strip("```")
    try:
        product_data = json.loads(json_text)
        print(product_data)
        return product_data
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)