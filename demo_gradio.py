import gradio as gr
from utils import *
from apis.api_openai import *
from apis.api_erniebot_baidu import get_erniebot_response

def get_answer_from_llm(user_input,api_tool=get_erniebot_response):
    fortune_message = get_fortune_message()
    prompt = fortune_teller_prompt_builder(user_input[2:],fortune_message)
    ai_answer = api_tool(prompt)
    return fortune_message,ai_answer

with gr.Blocks() as demo:
    gr.Markdown("<center><h1>AI求签问卜</h1></center>")
    with gr.Row():
        with gr.Column(scale=1, min_width=100):
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

    btn.click(get_answer_from_llm, inputs=input_text, outputs=[output_text0,output_text1])

demo.launch()

