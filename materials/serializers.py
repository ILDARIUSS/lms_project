from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Lesson
        fields = (
            'id',
            'course',
            'title',
            'description',
            'preview',
            'video_link',
            'owner',
        )
        validators = [VideoLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.id')
    subscribers_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'preview',
            'description',
            'owner',
            'updated_at',
            'lessons_count',
            'lessons',
            'subscribers_count',
            'is_subscribed',
        )

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_subscribers_count(self, obj):
        return obj.subscribers.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.subscribers.filter(id=request.user.id).exists()
        return False