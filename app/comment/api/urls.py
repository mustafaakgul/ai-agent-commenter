from django.urls import path
from app.comment.api.views import (
    CommentAPIView,
    UpdateAnsweredCommentsAPIView,
    CommentsByStatusAPIView,
    ApproveCommentAPIView
)


app_name = 'comment'


urlpatterns = [
    path('', CommentAPIView.as_view(), name='tasks'),
    path('status/filter', CommentsByStatusAPIView.as_view(), name='comments_by_status'),
    path('approve', ApproveCommentAPIView.as_view(), name='approve_comment'),
    path('update/answered', UpdateAnsweredCommentsAPIView.as_view(), name='update_answered_comments'),
]
