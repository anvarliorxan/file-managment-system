from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.user.serializers import FileUploadSerializer
from apps.user.serializers import FileListSerializer
from apps.user.serializers import FileUpdateSerializer
from apps.user.models import File
from django.http import FileResponse, Http404
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from apps.user.filter import FileFilter
from django_filters.rest_framework import DjangoFilterBackend


class FileUploadApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUpdateApi(APIView):

    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, *args, **kwargs):
        file = get_object_or_404(request.user.files.all(), pk=pk)

        serializer = FileUpdateSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response({"results": serializer.data}, status=status.HTTP_200_OK)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class GetFileApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        file = get_object_or_404(File, pk=pk)
        cache_key = f'{file.name}{file.pk}'
        views = cache.get(cache_key, 1)
        cache.set(cache_key, views + 1, timeout=None)

        serializer = FileListSerializer(file, context={"views": views})
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)


class FileDeleteApi(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, *args, **kwargs):
        file = get_object_or_404(request.user.files.all(), pk=pk)
        file.delete()
        return Response({'message': 'File deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class PublicFileListApi(generics.ListAPIView):
    queryset = File.objects.filter(type="public")
    serializer_class = FileListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileFilter


class MyFileListApi(generics.ListAPIView):
    serializer_class = FileListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileFilter
    def get_queryset(self):
        return File.objects.filter(user=self.request.user)


class FileDownloadApi(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            file_instance = File.objects.get(pk=pk)
            file_path = file_instance.file.path
            response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_instance.name}"'
            return response
        except File.DoesNotExist:
            raise Http404("File not found")
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class SharedFileDownloadApi(APIView):
    def get(self, request, token, *args, **kwargs):
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

        try:
            data = serializer.loads(token)

            file_id = data.get('file_id')

            file_instance = File.objects.get(id=file_id, type='private')

            file_path = file_instance.file.path
            response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_instance.name}"'
            return response

        except File.DoesNotExist:
            raise Http404("File not found")
        except SignatureExpired:
            return Response({'error': 'The download link has expired.'}, status=400)
        except BadSignature:
            return Response({'error': 'Invalid download link.'}, status=400)



