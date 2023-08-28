from dotenv import load_dotenv
# ↓にcreate_indexを後で追加
from .chatbot_engine import chat, create_index
from os.path import join, dirname
import os
from langchain.memory import ChatMessageHistory


def respond(message, chat_history, index):
    # historyはHumanMessageとAIMessageの要素が交互に並んだリスト
    history = ChatMessageHistory()
    for [user_message, ai_message] in chat_history:
        history.add_user_message(user_message)
        history.add_ai_message(ai_message)
    bot_message = chat(message, history, index)
    chat_history.append([message, bot_message])
    return chat_history


def initialize(message, chat_history):
    dotenv_path = join(dirname(__file__), '../.env')
    load_dotenv(dotenv_path)
    api_key = os.environ["OPENAI_API_KEY"]
    app_env = os.environ.get('APP_ENV', 'production')

    index = create_index()
    respond(message, chat_history, index)
    return chat_history

    # index = create_index()
