from rest_framework import serializers
from apps.user.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    file_id = serializers.IntegerField()
    class Meta:
        model = Comment
        fields = ['file_id', 'content']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)




class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content']