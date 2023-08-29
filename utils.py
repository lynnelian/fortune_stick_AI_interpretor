import random
import json

def get_question_index(num):
    pairs = {"1":"事业","2":"学业","3":"健康","4":"财运","5":"姻缘","6":"综合运势"}
    if isinstance(eval(num),int):
        return pairs[str(num)]

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

def fortune_teller_prompt_builder(aspect,fortune_message):
    prompt_eng = f"You are a chinese traditional fortune teller.\
        The user want to know the fortune in this aspect:{aspect}\
        The fortune stick the user draws is:{fortune_message}\
        Reply the user in mandarin Chinese with at least 200 characters."
    
    prompt = f"你是一个著名的算命大师，用户向您询问关于{aspect}方面的运势。\
    以下是他抽到的签文：{fortune_message}\
    请先解释签诗的含义，然后回答用户的问题。"

    return prompt