from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import BlogPostSerializer, CommentSerializer
from users.models import User
from .models import BlogPost, Comments


import json, redis
from users.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta


class CreatePost(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        """
        View to create a blog post.
        BODY PARAMETERS: body
        """
        user = request.user
        try:
            serializer = BlogPostSerializer(data=request.data, owner=user)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'New post created.','data': serializer.data},status=status.HTTP_201_CREATED)
            return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Your post details could not be created',
                                'error': f'{e}'}, 
                                status=status.HTTP_501_NOT_IMPLEMENTED)
        

class CreateComment(APIView):
    def post(self, request, post_id):
        """View to create a comment for a post.
        BODY PARAMETERS: post (the post_id), body
        """
        user = request.user
        post = BlogPost.objects.get(id=post_id)
        if not post:
            return Response({'message':"This post does not exist."}, status=status.HTTP_404_NOT_FOUND)
        try:
            serializer = CommentSerializer(data=request.data, owner=user)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'New post created.','data': serializer.data},status=status.HTTP_201_CREATED)
            return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Your post details could not be created',
                                'error': f'{e}'}, 
                                status=status.HTTP_501_NOT_IMPLEMENTED)
        

class PostDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, post_id):
        """
        View to retrieve a blog post
        PATH PARAMETERS: post (the post_id)
        """
        user = request.user
        try:
            post = BlogPost.objects.filter(id=post_id).prefetch_related('post')
            if not post:
                return Response({'message':"This post does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            post_serializer = BlogPostSerializer(post, many=True)
            print(post_serializer.data)
            return Response({'message': 'The post and comments:',
                                'post details': post_serializer.data,
                                },
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'The post details could not be retrieved',
                             'error': f'{e}'},
                             status=status.HTTP_501_NOT_IMPLEMENTED)
                        
        
    def put(self, request, post_id):
        """
        View to edit a blog post. Only the owner can delete it!!
        BODY PARAMETERS: post (the post_id), body
        """
        user = request.user
        post = BlogPost.objects.get(id=post_id, owner=user)
        try:
            if post:
                body = request.data.get('body', None)
                if body:
                    post.body = body
                    post.save
                    serializer = BlogPostSerializer(post)
                    return Response({'message': 'The post and comments:',
                                     'post details': serializer.data},
                                     status=status.HTTP_200_OK)
                # serializer = BlogPostSerializer(post, data=request.data)
                # if serializer.is_valid():
                #     serializer.save()
                #     return Response(serializer.data)
                # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'The post details could not be updated',
                             'error': f'{e}'},
                             status=status.HTTP_501_NOT_IMPLEMENTED)

    
    def delete(self, request, post_id):
        """
        View to delete a blog post. Only the owner can delete it!!
        PATH PARAMETERS: post_id (the post_id)
        """
        user = request.user
        try:
            post = BlogPost.objects.filter(id=post_id, owner=user)
            if not post:
                return Response({'message':"This post does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            post.delete()
            return Response({'message': 'The post has been successfully DELETED'},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message': 'The post details could not be retrieved',
                             'error': f'{e}'},
                             status=status.HTTP_501_NOT_IMPLEMENTED)
        

class CommentDetails(APIView):
    def delete(self, request, comment_id):
        """
        View to delete a comment. Only the owner can delete it!!
        PATH PARAMETERS NEEDED: comment_id (ID of the comment)
        """
        user = request.user
        try:
            comment = Comments.objects.filter(id=comment_id, owner=user)
            if not comment:
                return Response({'message':"This post does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            comment.delete()
            return Response({'message': 'The post has been successfully DELETED'},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message': 'The comment details could not be deleted',
                                'error': f'{e}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request, comment_id):
        """
        View to edit a comment. Only the owner can edit it!!
        PATH PARAMETERS: comment_id (the comment_id), 
        BODY PARAMETER: body
        """
        user = request.user
        comment = Comments.objects.get(id=comment_id, owner=user)
        try:
            if comment:
                body = request.data.get('body', None)
                if body:
                    comment.body = body
                    comment.save
                    serializer = CommentSerializer(comment)
                    return Response({'message': 'The post and comments:',
                                     'post details': serializer.data},
                                     status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'The post details could not be updated',
                             'error': f'{e}'},
                             status=status.HTTP_501_NOT_IMPLEMENTED)
        

class HomeFeed(APIView):
    def get(self, request):
        posts = BlogPost.objects.prefetch_related('post')
        if posts:
            serializer = BlogPostSerializer(posts, many=True)
            return Response({'message': 'The post and comments:',
                             'post details':serializer.data},
                             status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No post has been made',
                             'post details':serializer.data},
                             status=status.HTTP_204_NO_CONTENT)

