from flask import Flask, request, jsonify, url_for
import requests
import json
import re
import random
from flask import render_template

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get_answer", methods=["POST"])
def get_answer():
    user_input= request.json["question"]
    q_index = get_question_index(user_input)
    fortune_message = get_fortune_message()
    ai_answer = get_ai_answer(q_index,fortune_message)
    return jsonify({"answer": ai_answer})


def get_question_index(num):
    pairs = {"1":"事业","2":"学业","3":"健康","4":"财运","5":"姻缘","6":"综合运势"}
    if isinstance(eval(num),int):
        return pairs[str(num)]
    else:
        return None

def get_fortune_message():
    draw_num = random.randint(1, 100)
    with open('data/data','r',encoding='utf8') as f:
        messages = json.load(f)
    content = messages[str(draw_num)]
    title = content.split('\r\n')[0]
    poem = content.split('签诗：')[1].split('仙机')[0]
    fortune_message = title+'\n'+poem
    print(f"本次拿到的签文：\n\n{title}\n{poem}")
    return fortune_message


def get_ai_answer(aspect,fortune_message):
    api_key = "your_api_key_here"  # 将这里的内容替换成你的 OpenAI API 密钥
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = f"You are a chinese traditional fortune teller.\
        The user want to know the fortune in this aspect:{aspect}\
        The fortune stick the user draws is:{fortune_message}\
        Reply the user in mandarin Chinese with at least 200 characters."

    data = [{"role": "system", "content": prompt}]
    payload = {
    'model': "gpt-3.5-turbo",
    "messages": data,
    "temperature": 1
    #"max_tokens": 150
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=600)
    print(response)
    text = json.loads(response.text)['choices'][0]['message']['content']
    return text

if __name__ == "__main__":
    app.run(debug=True)