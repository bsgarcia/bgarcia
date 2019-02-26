from django.contrib import admin
from .models import Post, Comment


models = [
    Post,
    Comment,
]

admin.site.register(models)
