from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from .models import Comment, LikeComment
from .serializers import CommentSerializer

User = get_user_model()

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # если detail = True то в url добавляется id
    @action(['POST'], detail=False)
    def like(self, request):
        author_id = request.data.get("author")
        comment_id = request.data.get("comment")
        author = get_object_or_404(User, id = author_id)
        comment = get_object_or_404(Comment, id = comment_id)

        if LikeComment.objects.filter(author = author, comment = comment).exists():
            # если лайк есть
            LikeComment.objects.filter(author = author, comment = comment).delete()
            # удаляем
        else:
            # если лайка нет
            LikeComment.objects.create(author = author, comment = comment)
            # создаем
        return Response(status=201)



