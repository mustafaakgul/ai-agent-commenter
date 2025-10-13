from django.contrib import admin

from app.comment.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]
    list_display_links = ["id"]
    search_fields = ["id"]
    list_filter = ["created", "updated"]

    class Meta:
        model = Comment
