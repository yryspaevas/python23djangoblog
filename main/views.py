from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializers

User = get_user_model()

@api_view(['GET'])
def post_list(request):
    queryset = Post.objects.all().order_by('id')
    # print('queryset: ', queryset)
    # queryset:  <QuerySet [<Post: Post object (2)>, <Post: Post object (3)>, <Post: Post object (4)>, <Post: Post object (5)>]>

    serializer = PostSerializers(queryset, many=True)
    # print("serializer data: ", serializer.data)
    # serializer data:  [OrderedDict([('id', 2), ('body', '2 post'), ('created_at', '2022-11-29T05:38:53.384755Z'), ('author', 'admin')]), OrderedDict([('id', 3), ('body', '3 post'), ('created_at', '2022-11-29T05:39:00.379975Z'), ('author', 'admin')]), OrderedDict([('id', 4), ('body', 'hello'), ('created_at', '2022-11-29T06:06:34.142357Z'), ('author', 'admin')]), OrderedDict([('id', 5), ('body', 'hello'), ('created_at', '2022-11-29T06:09:57.217381Z'), ('author', 'admin')])]

    return Response(serializer.data, 200)

@api_view(['POST'])
def create_post(request):
    serializer =PostSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(201)

@api_view(['PATCH'])
def update_post(request, id):
    post = get_object_or_404(Post, id = id)
    serializer = PostSerializers(instance=post, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(201)


@api_view(['DELETE'])
def delete_post(request, id):
    post = get_object_or_404(Post, id = id)
    res =  post.delete()
    return Response(204)
    

@api_view(['GET'])
def filter_by_user(request, u_id):
    # queryset = Post.objects.filter(author__id=u_id)
    author = get_object_or_404(User, id = u_id)
    queryset = Post.objects.filter(author=author)
    serializer = PostSerializers(queryset, many=True)
    return Response(serializer.data, 200)

@api_view(['GET'])
def search(request):
    q = request.query_params.get('q')
    queryset = Post.objects.filter(body__icontains=q)
    serializer = PostSerializers(queryset, many=True)
    return Response(serializer.data, 200)