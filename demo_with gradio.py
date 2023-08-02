import gradio as gr
import requests
import json
import random


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
    #print(f"本次拿到的签文：\n\n{title}\n{poem}")
    return fortune_message

def get_ai_answer(aspect,fortune_message):
    api_key = " "  # 将这里的内容替换成你的 OpenAI API 密钥
    url = "https://proxy.aido.ai/v1/chat/completions" #大神提供的转接gpt服务器
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = f"You are a chinese traditional fortune teller.\
        The user want to know the fortune in this aspect:{aspect}\
        The fortune stick the user draws is:{fortune_message}\
        Reply the user in mandarin Chinese with at least 200 characters."

    data = [{"role": "user", "content": prompt}]
    payload = {
    'model': "gpt-3.5-turbo",
    "messages": data,
    "temperature": 1
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=600)
    print(response)
    text = json.loads(response.text)['choices'][0]['message']['content']
    return text

def get_answer_from_py(user_input):
    #q_index = get_question_index(user_input)
    fortune_message = get_fortune_message()
    ai_answer = get_ai_answer(user_input[2:],fortune_message)
    return fortune_message,ai_answer

with gr.Blocks() as demo:
    gr.Markdown("<center><h1>AI求签问卜</h1></center>")
    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            img1 = gr.Image("./data/pic.png")
        with gr.Column(scale=1, min_width=600):
            gr.Markdown(
            '''
            </br>
            说明：
            <h3>求签前先默念“大仙大仙，请指点迷津”并禀报求问之事：中文全名、信男（信女）、岁数（虚龄）、向大仙禀报求问之事。</h3>
            <h3>大仙可以为你解读以下方面的运势：1、 事业 2、学业 3、健康 4、财运 5、姻缘 6、综合运势</h3>
            '''
            )
        options = ["1 事业", "2 学业", "3 健康","4 财运","5 姻缘","6 综合运势"]
        with gr.Column(scale=1, min_width=600):
            input_text = gr.Dropdown(options, label="请选择方向：")
            btn = gr.Button("提交").style(full_width=True)
        with gr.Column(scale=1, min_width=600):
            output_text0 = gr.Textbox(lines=4, label="本次拿到的签文：")
        with gr.Column(scale=1, min_width=600):
            output_text1 = gr.Textbox(lines=5, label="AI大仙解答：")

    btn.click(get_answer_from_py, inputs=input_text, outputs=[output_text0,output_text1])

demo.launch()

