"""
conda create -n azure-openai
conda activate azure-openai
conda install python azure-identity openai flask pandas openpyxl -c conda-forge

Please visit https://aka.ms/azure-dev for installation instructions and then,once installed, authenticate to your Azure account using 'azd auth login'.

python example_ncus.py

"""

import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from config_ncus import *

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",
)

completion = client.chat.completions.create(
    model=deployment,
    messages= [
    {
      "role": "user",
      "content": "How to Choose the Right MEMS Microphone Interface, Analog or Digital?"
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
            "query_type": "vector_semantic_hybrid",
            "fields_mapping": {},
            "in_scope": True,
            "role_information": "You are an AI assistant that helps people find information.",
            "filter": None,
            "strictness": 3,
            # "top_n_documents": 5,
            "top_n_documents": 2,
            "authentication": {
              "type": "api_key",
              "key": f"{search_key}"
            },
            "embedding_dependency": {
              "type": "deployment_name",
              "deployment_name": f"{vector_deployment}"
            }
          }
        }]
    }
)
details = open('details.json', 'w')
details.write(completion.to_json())
details.close()
# print(completion.to_json())
print(f"Answer: {completion.choices[0].message.content}")
print(f"Citation: {completion.choices[0].message.context['citations'][0]['title']}")
print(f"Tokens Used: {completion.usage.total_tokens}")
 