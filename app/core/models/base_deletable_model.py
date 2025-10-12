from django.db import models


class BaseDeletableModel(models.Model):
    """
    Base model that provides common fields for all models with soft delete functionality.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")
    deleted = models.DateTimeField(null=True, blank=True, verbose_name="deleted")
    is_deleted = models.BooleanField(default=False, verbose_name="is_deleted")

    class Meta:
        abstract = True
        ordering = ['-created']
        verbose_name = "Base Deletable Model"
        verbose_name_plural = "Base Deletable Models"
