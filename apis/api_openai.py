import requests
import json

def get_openai_response(prompt):
    api_key = "your_api_key_here"  # 将这里的内容替换成你的 OpenAI API 密钥
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "system", "content": prompt}],
    "temperature": 1
    #"max_tokens": 150
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=600)
    print(response)
    text = json.loads(response.text)['choices'][0]['message']['content']
    return text