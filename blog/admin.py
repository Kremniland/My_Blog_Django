from django.contrib import admin

from .models import Category, Post, ContactModel, Comments


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    list_display_links = ['title']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'create_date', 'update_date', 'publisher']
    list_display_links = ['title']
    list_filter = ['publisher']


@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'create_date']


@admin.register(Comments)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'create_date', 'post', 'status']




