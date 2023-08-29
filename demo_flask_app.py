from flask import Flask, request, jsonify
from flask import render_template
from utils import *
from apis.api_openai import get_openai_response
from apis.api_erniebot_baidu import get_erniebot_response

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get_answer_from_llm", methods=["POST"])
def get_answer_from_llm(api_tool=get_erniebot_response):
    user_input= request.json["question"]
    fortune_message = get_fortune_message()
    prompt = fortune_teller_prompt_builder(get_question_index(user_input),fortune_message)
    ai_answer = api_tool(prompt)
    return jsonify({"answer": ai_answer})

if __name__ == "__main__":
    app.run(debug=True)