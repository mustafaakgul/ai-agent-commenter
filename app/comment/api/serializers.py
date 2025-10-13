from rest_framework.serializers import ModelSerializer

from app.comment.models import Comment


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'customer_id',
            'product_name',
            'content_id',
            'content',
            'web_url',
            'response',
            'status'
        ]


class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
