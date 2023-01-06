from django.contrib import admin

from django.utils.safestring import mark_safe

from .models import Category, Post, ContactModel, Comments


class PostInline(admin.StackedInline):
    '''Добавление и вывод коментариев к постам в админке '''
    model = Comments
    extra = 3



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    list_display_links = ['title']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'image_show', 'create_date', 'update_date', 'publisher']
    list_display_links = ['title']
    list_filter = ['publisher']
    inlines = [PostInline]

    def image_show(self, obj):
        '''Вывод маленькой картинки в админке'''
        if obj.image:
            return mark_safe("<img src='{}' width='60' />".format(obj.image.url))
        return None



@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'create_date']


@admin.register(Comments)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'create_date', 'post', 'status']




