from rest_framework import routers
from .views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = []

urlpatterns += router.urls
