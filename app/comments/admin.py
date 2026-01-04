from django.contrib import admin

from app.comments.models import Comment, CommentAnalyzer


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]
    list_display_links = ["id"]
    search_fields = ["id"]
    list_filter = ["created", "updated"]

    class Meta:
        model = Comment


@admin.register(CommentAnalyzer)
class CommentAnalyzerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CommentAnalyzer._meta.fields]
    list_display_links = ["id"]
    search_fields = ["id"]
    list_filter = ["created", "updated"]

    class Meta:
        model = CommentAnalyzer
