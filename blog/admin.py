from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import (
    Post, Category, Link, Comment, Bbscomment, Bbstitle
)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'created_at')

class LinkAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'url', 'created_at')

class BbstitleAdmin(admin.ModelAdmin):
    list_display=('id','maintitle', 'subtitle', 'created_at')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Comment, MarkdownxModelAdmin)
admin.site.register(Bbstitle, BbstitleAdmin)
admin.site.register(Bbscomment, MarkdownxModelAdmin)
