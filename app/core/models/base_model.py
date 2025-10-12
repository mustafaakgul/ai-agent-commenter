from django.db import models


class BaseModel(models.Model):
    """
    Base model that provides common fields for all models.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")

    class Meta:
        abstract = True
        ordering = ['-created']
        verbose_name = "Base Model"
        verbose_name_plural = "Base Models"
