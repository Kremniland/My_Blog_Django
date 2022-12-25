from django import template
from blog.models import Category, Post

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.prefetch_related('post').all()


@register.inclusion_tag('blog/list_categories.html') # HTML файл который будем встраивать в шаблон
def show_categories():
    cats = Category.objects.all()
    return {'cats': cats}