from flask import Flask, request, jsonify, url_for
import requests
import json
from flask import render_template

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get_answer", methods=["POST"])
def get_answer():
    question = request.json["question"]
    ai_answer = get_ai_answer(question)

    return jsonify({"answer": ai_answer})

def get_ai_answer(question):
    api_key = "your_api_key_here"  # 将这里的内容替换成你的 OpenAI API 密钥
    api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    prompt = f"回答并解释以下算卦问题：{question}"

    data = {
        "prompt": prompt,
        "max_tokens": 150,
        "n": 1,
        "stop": None,
        "temperature": 1
    }

    payload = {
        'model': "gpt-3.5-turbo",
        "messages": data,
        "temperature": 0
    }

    response = requests.post(api_url, headers=headers, json=data)
    response_json = response.json()
    
    return response_json["choices"][0]["text"].strip()

if __name__ == "__main__":
    app.run(debug=True)