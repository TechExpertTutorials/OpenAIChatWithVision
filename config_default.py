import os

search_key = os.getenv("SEARCH_KEY", "[search-resource-key]")
endpoint = os.getenv("ENDPOINT_URL", "https://[openai-service-name].azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "[llm-model]")
vector_deployment = os.getenv("TEXT_DEPLOYMENT_NAME", "[embedding-model]")
search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://[search-service-name].search.windows.net")
search_index = os.getenv("SEARCH_INDEX_NAME", "[search-index-name]")