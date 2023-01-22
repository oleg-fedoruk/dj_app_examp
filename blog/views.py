from django.db.models import Subquery, OuterRef
from django.db.models.functions import JSONObject
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, ListPostSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка постов и отдельного поста"""
    queryset = Post.objects.all()

    def get_queryset(self):
        if self.action == 'list':
            last_comment = Subquery(Comment.objects.filter(post_id=OuterRef("id"), ).order_by("-date_created").values(
                data=JSONObject(pk="pk", text="text"))[:1])
            posts = Post.objects.annotate(last_comment=last_comment).all()
        elif self.action == 'retrieve':
            posts = Post.objects.all()
        return posts

    def get_serializer_class(self):
        if self.action == 'list':
            return ListPostSerializer
        elif self.action == 'retrieve':
            return PostSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # увеличение количества просмотров конктретного поста
        instance.views += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр всех комментариев"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
