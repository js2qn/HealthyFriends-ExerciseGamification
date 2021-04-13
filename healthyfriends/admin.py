from django.contrib import admin

from .models import Videos, ForumPost, Discussion
# Register your models here.
admin.site.register(Videos)
admin.site.register(ForumPost)
admin.site.register(Discussion)