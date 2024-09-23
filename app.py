"""

python app.py
http://127.0.0.1:5000/
 
"""
 
from flask import Flask, request, render_template_string
import requests
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from config_ncus import *
 
app = Flask(__name__)

# HTML template for the form
form_template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Your Production Application</title>
  </head>
  <body>
    <center>
    <h1>Company Chatbot</h1>
    <h2>Enter Your Question</h2>
    <form method="post">
      <label for="input_data">Input:</label>
      <input type="text" id="input_data" name="input_data" size="50">
      <button type="submit">Submit</button>
    </form>
    {% if result %}
      <h2>Result from API:</h2>
      <p>{{ result }}</p>
    {% endif %}
  </body>
</html>
'''
 
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        input_data = request.form['input_data']
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://cognitiveservices.azure.com/.default")
           
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2024-05-01-preview",
        )
 
        completion = client.chat.completions.create(
            model=deployment,
            messages= [
            {
                "role": "user",
                "content": input_data
            }],
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False,
            extra_body={
            "data_sources": [{
                "type": "azure_search",
                "parameters": {
                    "endpoint": f"{search_endpoint}",
                    "index_name": f"{search_index}",
                    "semantic_configuration": "default",
                    "query_type": "semantic",
                    "fields_mapping": {},
                    "in_scope": True,
                    "role_information": "You are an AI assistant that helps people find information.",
                    "filter": None,
                    "strictness": 3,
                    "top_n_documents": 5,
                    "authentication": {
                    "type": "api_key",
                    "key": f"{search_key}"
                    }
                }
                }]
            }
        )
        result = completion.choices[0].message.content
 
        """
        # Replace 'https://api.example.com/endpoint' with the actual API URL
        api_url = 'https://api.example.com/endpoint'
        response = requests.post(api_url, json={'data': input_data})
        if response.status_code == 200:
            result = response.json()
        else:
            result = 'Error: Could not retrieve data from API'
        """
 
    return render_template_string(form_template, result=result)
 
if __name__ == '__main__':
    app.run(debug=True)