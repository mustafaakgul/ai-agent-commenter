from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.comment.api.serializers import CommentCreateSerializer, CommentListSerializer
from app.comment.models import Comment
from integrations.ai.agents.agent_comment.langchain import creator


class CommentAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        query = Comment.objects.all()
        serializer = CommentListSerializer(query, many=True)

        resp = {
            'status': 'true',
            'message': 'successful',
            'payload': serializer.data
        }
        response = Response(data=resp, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()

            ## LLM Request
            creator.create(obj.id, obj.content)

            resp = {
                'status': 'true',
                'message': 'successful',
                'payload': serializer.data
            }
            response = Response(data=resp, status=status.HTTP_201_CREATED)
            return response

        resp = {
            'status': 'false',
            'message': 'error',
            'payload': serializer.errors
        }
        return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)


class ApprovedCommentsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        query = Comment.objects.filter(status='APPROVED')
        serializer = CommentListSerializer(query, many=True)

        resp = {
            'status': 'true',
            'message': 'successful',
            'payload': serializer.data
        }
        response = Response(data=resp, status=status.HTTP_200_OK)
        return response
