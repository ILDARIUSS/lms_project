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

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'preview',
            'description',
            'owner',
            'lessons_count',
            'lessons',
        )

    def get_lessons_count(self, obj):
        return obj.lessons.count()