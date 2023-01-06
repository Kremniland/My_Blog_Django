from rest_framework import serializers

from .models import Post, Category


class CategorySerializer(serializers.ModelSerializer):
    class Mets:
        model = Category
        fields = ('__all__')


class PostSerializer(serializers.ModelSerializer):

    # category = CategorySerializer(read_only=True, many=False)
    # category_title = serializers.CharField(source='category_title')

    class Meta:
        model = Post
        fields = '__all__'



