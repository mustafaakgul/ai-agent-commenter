from django.db import models

from app.comment.enums import AGENT_STATUS
from app.core.models.base_model import BaseModel


class Comment(BaseModel):
    customer_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    content_id = models.CharField(max_length=50)
    content = models.TextField()
    web_url = models.URLField()
    response = models.TextField(default="temp", max_length=5000)
    status = models.CharField(max_length=50, choices=AGENT_STATUS)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment {self.id} at {self.created}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class CommentAnalyzer(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="analyzers")
    analyzed_at = models.DateTimeField(auto_now_add=True)

    # Analysis Results
    sentiment = models.CharField(max_length=50)
    sentiment_score = models.FloatField()
    category = models.CharField(max_length=100)
    urgency = models.CharField(max_length=50)
    keywords = models.TextField()  # Comma-separated keywords
    summary = models.TextField()
    main_issue = models.TextField()
    required_action = models.BooleanField()
    response_tone = models.CharField(max_length=50)

    # Response Results
    response = models.TextField()

    # Quality Control Results
    quality_control = models.TextField()

    def __str__(self):
        return f"CommentAnalyzer {self.id} for Comment {self.comment.id}"

    class Meta:
        verbose_name = "Comment Analyzer"
        verbose_name_plural = "Comment Analyzers"
