from apps.email.models import Email
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .tasks import send_review_email_task

@api_view(['GET', 'POST'])
def send_subscription_email(request):
    if request.method == 'POST':
        email = Email(name=request.data['name'],email=request.data['email'],review=request.data['review'])
        email.save()
        msg = "Thank for your review !!!"
        send_review_email_task.delay(request.data['name'],request.data['email'],request.data['review'])
        return HttpResponse(msg)
    return JsonResponse({"message": "Hello, world!"})

