from rest_framework import serializers
from .models import BlogPost, Comments
import json


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'post', 'body', 'likes']


    def __init__(self, *args, **kwargs):
        # Extract the additional 'owner' argument
        self.owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        # Ensure the owner is set when creating the comment
        validated_data['owner'] = self.owner
        return super().create(validated_data)
    


class BlogPostSerializer(serializers.ModelSerializer):
    name_of_owner = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField()  # Show username or string representation of owner
    post_comments = CommentSerializer(many=True, read_only=True, source='post')  # Related comments

    class Meta:
        model = BlogPost
        fields = ['id', 'owner', 'body', 'likes', 'name_of_owner', 'post_comments', 'number_of_comments']

    def get_name_of_owner(self, object):
        return str(object.owner.username)
    
    def get_number_of_comments(self, object):
        return (object.post).count()
    
    # to add the current user as the owner of the post
    def __init__(self, *args, **kwargs):
        # Extract the additional 'owner' argument
        self.owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        # Ensure the owner is set when creating the post
        validated_data['owner'] = self.owner
        return super().create(validated_data)
    
