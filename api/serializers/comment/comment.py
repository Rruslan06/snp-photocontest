from rest_framework import serializers
from models_app.models import Comment

class CommentSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(source='author.username', read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
   
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        
        fields = ['id', 'text', 'date', 'author_name', 'parent', 'author', 'photo', 'replies']
        read_only_fields = ['photo']

    
    def get_replies(self, obj):

        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
        return []
    
    