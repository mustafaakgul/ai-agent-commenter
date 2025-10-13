from django.urls import path
from app.comment.api.views import CommentAPIView


app_name = 'comment'


urlpatterns = [
    path('', CommentAPIView.as_view(), name='tasks'),
]
