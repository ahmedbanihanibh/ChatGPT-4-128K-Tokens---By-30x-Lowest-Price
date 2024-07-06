import requests
import sseclient
import json

# Define the endpoint and headers
url = "https://chatgpt-4-128k-tokens-by-30x-lowest-price.p.rapidapi.com/chat"
headers = {
  #Add the X-Rapidapi-Key with the new Key you have after subscribing to the Api.
    "X-Rapidapi-Key": "",
    "X-Rapidapi-Host": "chatgpt-4-128k-tokens-by-30x-lowest-price.p.rapidapi.com",
    "Content-Type": "application/json",
    "Host": "chatgpt-4-128k-tokens-by-30x-lowest-price.p.rapidapi.com"
}

# Define the payload
payload = {
    "model": "gpt-4o",
    "stream": True,
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Tell me a long Story!"
        }
    ]
}

# Make the request and handle the stream response
response = requests.post(url, headers=headers, json=payload, stream=True)

# Ensure the response is an event stream
if response.status_code == 200:
    #print("Connected to the API successfully.")
    client = sseclient.SSEClient(response)
    for event in client.events():
        try:
            #print("Received an event.")
            raw_data = event.data.strip()
            if raw_data == "[DONE]":
                #print("Stream ended.")
                break
            if raw_data.startswith("data: "):
                raw_data = raw_data[len("data: "):]
            if raw_data :  # Ensure raw_data is not empty
                #print(f"Event data: {raw_data}")

                if(raw_data != "[DONE]"):
                 data = json.loads(raw_data)
                if 'choices' in data and len(data['choices']) > 0:
                    delta = data['choices'][0].get('delta', {})
                    content = delta.get('content', '')
                    if content:
                        print(content, end='', flush=True)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            continue
else:
    print(f"Error: {response.status_code}")
    print(response.text)
