from .chat_app import initialize
from django.contrib import messages
from django.shortcuts import render
import datetime
from ai_chatbot.models import Log

chat_history = []


def chat_log(input_data, request, chat_session):
    # チャットbotと会話する関数を呼び出す
    logs = initialize(input_data, chat_history)

    # 過去の入力内容と処理結果のタプルを追加
    # 更新したchat_sessionをセッションに保存
    chat_session.append(logs[-1])

    # 更新したchat_sessionをセッションに保存
    request.session['chat_session'] = chat_session
    print(f'chat_sessionは{chat_session}')

    # 結果をテンプレートに表示する
    return render(
        request, 'ai_chatbot/chat.html',
        {
            'chat_session': chat_session,
        },
        )


def log_save(request, chat_session):
    user_name = request.user.username
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    title = chat_session[0][0]
    chat_session[0][0] = ''

    if user_name == '':
        user_name = 'guest'
        title += '（ゲスト）'

    # リスト内包表記を使用して各要素を改行で結合し、一つの文字列にする
    log = '\n\n'.join(['\n\n'.join(chat) for chat in chat_session])

    # chat_sessionの初期化
    chat_session = []

    # モデルのインスタンスを作成してデータベースに保存
    my_model_instance = Log(
        user_name=user_name,
        title=title,
        text=log, date=date
        )
    my_model_instance.save()
    messages.success(request, 'ログを保存しました。')
