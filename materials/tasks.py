from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from materials.models import Course


@shared_task
def send_course_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return "Course not found"

    emails = course.subscribers.values_list('email', flat=True)

    if not emails:
        return "No subscribers"

    send_mail(
        subject=f'Обновление курса: {course.title}',
        message=f'Курс "{course.title}" был обновлен.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=list(emails),
        fail_silently=True,
    )

    return f"Emails sent: {len(emails)}"