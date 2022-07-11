from rest_framework import serializers
from .models import *


# class ProductSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     price = serializers.DecimalField(max_digits=10, decimal_places=2)
#     image = serializers.ImageField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ['id','name', 'price', 'image']
        fields = '__all__'

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
            return rep


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'price', 'image']
        # fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = ['author', 'text', 'create_date', 'id']

    def create(self, validated_data):
        requset = self.context.get('request')
        user = requset.user
        validated_data['author'] = user

        return super().create(validated_data)