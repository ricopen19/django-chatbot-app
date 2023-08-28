from django.urls import path
from ai_chatbot.views import (
    LogListView,
    LogDetailView,
    LogCreateView,
    LogDeleteView,
    LogUpdateView,
    post,
    delete_file,
    delete_chat
)

urlpatterns = [
    path('log/list', LogListView.as_view(), name='log-list'),
    path('log/<int:pk>/', LogDetailView.as_view(), name='log-detail'),
    path('log/new/', LogCreateView.as_view(), name='log-new'),
    path('log/delete/', LogDeleteView.as_view(), name='log-delete'),
    path('log/<int:pk>/edit/', LogUpdateView.as_view(), name='log-edit'),
    path('', post, name='chat-view'),
    path('delete/<int:file_id>/', delete_file, name='file-delete'),
    path('delete/chat', delete_chat, name='chat-delete'),
]
