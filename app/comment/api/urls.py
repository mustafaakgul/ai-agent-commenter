from django.urls import path
from app.comment.api.views import CommentAPIView, ApprovedCommentsAPIView, UpdateAnsweredCommentsAPIView, CommentsByStatusAPIView


app_name = 'comment'


urlpatterns = [
    path('', CommentAPIView.as_view(), name='tasks'),
    path('status/approved', ApprovedCommentsAPIView.as_view(), name='approved_comments'),
    path('status/filter', CommentsByStatusAPIView.as_view(), name='comments_by_status'),
    path('update/answered', UpdateAnsweredCommentsAPIView.as_view(), name='update_answered_comments'),
]
