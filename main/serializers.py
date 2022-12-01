from rest_framework.serializers import ModelSerializer
from .models import Post
from reviews.serializers import CommentSerializer

class PostSerializers(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance:Post):
        # print("instance: ", instance)
        # instance:  Post object (2)
        # repr:  OrderedDict([('id', 2), ('body', '2 post'), ('created_at', '2022-11-29T05:38:53.384755Z'), ('author', 1)])
        # instance:  Post object (3)
        # repr:  OrderedDict([('id', 3), ('body', '3 post'), ('created_at', '2022-11-29T05:39:00.379975Z'), ('author', 1)])
        # instance:  Post object (4)
        # repr:  OrderedDict([('id', 4), ('body', 'hello'), ('created_at', '2022-11-29T06:06:34.142357Z'), ('author', 1)])
        # instance:  Post object (5)

        rep = super().to_representation(instance)
        # print('repr: ', rep)
        rep['author'] = instance.author.username
        
        # comments = instance.comments.all()
        
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data #комментарий и информация о нем
        rep['comments'] = instance.comments.count() # количество комментариев к каждому посту
        return rep 