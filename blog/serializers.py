from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    class Meta:
        model = Comment
        fields = ('pk', 'text')


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода отдельного поста со списком комментариев"""
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('pk', 'title', 'text', 'views', 'date_created', 'comments')


class ListPostSerializer(serializers.ModelSerializer):
    """Сериализатор для списка постов с выводом pk и текста последнего комментария"""
    last_comment_pk = serializers.IntegerField(source='last_comment.pk', read_only=True)
    last_comment_text = serializers.CharField(source='last_comment.text', read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'text', 'views', 'date_created', 'last_comment_pk', 'last_comment_text')
