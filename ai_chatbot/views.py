from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View,
)
from ai_chatbot.models import Log, File
# 処理が終わった後に指定のページに飛ばす機能
from django.urls import reverse_lazy
# クラスに継承させるとその機能を使うのにログイン認証が必要となる（※最初に継承させる）
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import MyForm, UploadForm
from django.contrib import messages
from django.db.models import Q
from .function import chat_log, log_save
import os


class LogListView(ListView):
    model = Log
    template_name = 'ai_chatbot/log_list.html'
    context_object_name = 'logs'

    def get_queryset(self):
        # ログインユーザーが作成したリストのみを取得
        return Log.objects.filter(Q(user_name=self.request.user) | Q(user_name='guest'))


class LogDetailView(DetailView):
    model = Log
    template_name = 'ai_chatbot/log_detail.html'


class LogCreateView(LoginRequiredMixin, CreateView):
    model = Log
    # テーブルの中で作る列(=field)を指定する
    fields = ['user_name', 'title', 'text', 'date']

    def get_user(request):
        user_name = request.user.username
        return user_name

    # logが出来た後どのURLへ遷移するか
    success_url = reverse_lazy('log-list')


class LogDeleteView(LoginRequiredMixin, View):
    model = Log

    def post(self, request):
        log_ids = request.POST.getlist('log_ids')
        for log_id in log_ids:
            log = get_object_or_404(Log, id=log_id)
            log.delete()

        return redirect(reverse('log-list'))


class LogUpdateView(LoginRequiredMixin, UpdateView):
    model = Log
    # テーブルの中で編集する列(=field)を指定する
    fields = ['title', 'text', 'date']
    success_url = reverse_lazy('log-list')


def post(request):
    file_form = UploadForm(request.POST, request.FILES or None)
    log_form = MyForm(request.POST)

    # セッションから過去にユーザーが入力した内容を取得し、chat_sessionに保存
    # chat_sessionが存在しない場合は空のリスト[]を返す
    chat_session = request.session.get('chat_session', [])
    # フォームのデータを受け取りバリデーション
    action = request.POST.get('action')

    # ユーザーがフォームに入力したデータを取得しchat_sessionに保存
    input_data = request.POST.get('input_data', '')

    if request.method == 'POST':
        # フォームのデータを受け取りバリデーション
        action = request.POST.get('action')

        # ユーザーがフォームに入力したデータを取得しchat_sessionに保存
        input_data = request.POST.get('input_data', '')

        if action == 'send' and input_data != "":
            # フォームのデータがバリデーションに成功した場合
            if log_form.is_valid():
                # チャットのログを出力する関数
                chat_log(input_data, request, chat_session)

        elif action == 'save' and len(chat_session) > 0:
            # logを保存する関数
            log_save(request, chat_session)

        elif action == 'upload':
            if file_form.is_valid():
                file = file_form.cleaned_data['file']
                file_name = file.name
                uploaded_file = File(file_name=file_name, file=file)
                # uploaded_file = file_form.save(commit=False)
                # uploaded_file.name = name
                uploaded_file.save()

                messages.success(request, 'アップロードに成功しました')
                file_form = UploadForm()
            else:
                messages.error(request, 'ファイルをアップロードしてください')

        # ログがない状態で送信された場合
        else:
            if len(input_data) == 0:
                messages.error(request, 'メッセージを入力してください')
            if len(chat_session) == 0:
                messages.error(request, '保存するログがありません')

    # formの入力欄を空白にする
    log_form = MyForm()

    files = File.objects.all()

    context = {
        'files': files,
        'file_form': file_form,
        'log_form': log_form,
        'chat_session': chat_session,
        }

    return render(request, 'ai_chatbot/chat.html', context)


def delete_file(request, file_id):
    try:
        uploaded_file = File.objects.get(id=file_id)
        file_path = uploaded_file.file.path  # ファイルのパスを取得
        os.remove(file_path)  # ファイルを削除
        uploaded_file.delete()  # データベースからもファイル情報を削除
    except File.DoesNotExist:
        pass  # ファイルが存在しない場合は何もしない

    return redirect('chat-view')


def delete_chat(request):
    file_form = UploadForm(request.POST, request.FILES or None)
    log_form = MyForm(request.POST)
    files = File.objects.all()
    chat_session = []

    context = {
        'files': files,
        'file_form': file_form,
        'log_form': log_form,
        'chat_session': chat_session,
        }

    return render(request, 'ai_chatbot/chat.html', context)
