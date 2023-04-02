from flask import Flask, render_template, request, redirect, url_for, g, make_response
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("API_KEY")
model_id = 'gpt-3.5-turbo'

app = Flask(__name__)

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )

    conversation.append(
        {'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    
    total_tokens = response['usage']['total_tokens']

    return conversation, total_tokens

@app.before_request
def init_conversation():
    if not hasattr(g, 'conversation'):
        g.conversation = []
        g.conversation.append({'role': 'system', 'content': 'How may I help you?'})
        g.conversation, g.total_tokens = ChatGPT_conversation(g.conversation)

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        g.conversation.append({'role': 'user', 'content': user_input})
        g.conversation, tokens_used = ChatGPT_conversation(g.conversation)
        g.total_tokens += tokens_used

    return render_template('chat.html', conversation=g.conversation, total_tokens=g.total_tokens)

if __name__ == '__main__':
    app.run(debug=True)
