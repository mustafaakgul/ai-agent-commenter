from rest_framework.serializers import ModelSerializer

from app.comment.models import Comment, CommentAnalyzer, CommentQualityScore


class CommentAnalyzerSerializer(ModelSerializer):
    class Meta:
        model = CommentAnalyzer
        exclude = ['comment']  # Exclude the foreign key to avoid recursion


class CommentQualityScoreSerializer(ModelSerializer):
    class Meta:
        model = CommentQualityScore
        exclude = ['comment']  # Exclude the foreign key to avoid recursion


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


class CommentDetailSerializer(ModelSerializer):
    analyzers = CommentAnalyzerSerializer(many=True, read_only=True)
    quality_score = CommentQualityScoreSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
