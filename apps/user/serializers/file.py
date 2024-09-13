from rest_framework import serializers
from apps.user.models import File
from apps.user.models import Hashtag
from apps.user.serializers.comment import CommentListSerializer


class HashtagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name']


class FileUploadSerializer(serializers.ModelSerializer):
    hashtags = serializers.PrimaryKeyRelatedField(
        queryset=Hashtag.objects.all(), many=True
    )
    class Meta:
        model = File
        fields = ['file', 'type', 'description', 'hashtags', 'expiration_date']


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        hashtags = validated_data.pop('hashtags')

        file = File.objects.create(**validated_data)
        file.hashtags.set(hashtags)
        return file




class FileUpdateSerializer(serializers.ModelSerializer):
    hashtags = serializers.PrimaryKeyRelatedField(
        queryset=Hashtag.objects.all(), many=True
    )
    class Meta:
        model = File
        fields = ['file', 'type', 'description', 'hashtags']

    def update(self, instance, validated_data):
        instance.file = validated_data.get('file', instance.file)
        instance.type = validated_data.get('type', instance.type)
        instance.description = validated_data.get('description', instance.description)

        hashtags = validated_data.pop('hashtags')
        instance.hashtags.set(hashtags)

        instance.save()
        return instance



class FileListSerializer(serializers.ModelSerializer):
    comments = CommentListSerializer(many=True, read_only=True)
    hashtags = HashtagListSerializer(many=True, read_only=True)
    views = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'type', 'created', 'modified', 'share_link', 'comments', 'views', 'hashtags']

    def get_views(self, obj):
        return self.context.get('views', 0)




