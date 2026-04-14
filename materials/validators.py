from rest_framework import serializers


class VideoLinkValidator:
    def __init__(self, field: str):
        self.field = field

    def __call__(self, value):
        video_link = value.get(self.field)

        if not video_link:
            return

        allowed_domains = (
            'youtube.com',
            'www.youtube.com',
            'youtu.be',
            'www.youtu.be',
        )

        if not any(domain in video_link for domain in allowed_domains):
            raise serializers.ValidationError(
                'Разрешены ссылки только на YouTube.'
            )