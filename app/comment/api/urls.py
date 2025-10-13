from django.urls import path
from app.comment.api.views import CommentAPIView, ApprovedCommentsAPIView


app_name = 'comment'


urlpatterns = [
    path('', CommentAPIView.as_view(), name='tasks'),
    path('status/approved/', ApprovedCommentsAPIView.as_view(), name='approved_comments'),
]
