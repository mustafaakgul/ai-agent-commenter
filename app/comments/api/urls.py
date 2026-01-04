from django.urls import path
from app.comments.api.views import (
    CommentAPIView,
    UpdateAnsweredCommentsAPIView,
    CommentsByStatusAPIView,
    ApproveCommentAPIView,
    CommentDetailAPIView
)


app_name = 'comments'


urlpatterns = [
    path('', CommentAPIView.as_view(), name='tasks'),
    path('<int:comment_id>', CommentDetailAPIView.as_view(), name='comment_detail'),
    path('status/filter', CommentsByStatusAPIView.as_view(), name='comments_by_status'),
    path('approve', ApproveCommentAPIView.as_view(), name='approve_comment'),
    path('update/answered', UpdateAnsweredCommentsAPIView.as_view(), name='update_answered_comments'),
]
