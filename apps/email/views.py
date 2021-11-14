from apps.email.models import Email
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.http import JsonResponse

from apps.email.serializers import EmailSerializer
from .tasks import send_review_email_task
from rest_framework.viewsets import ModelViewSet

@api_view(['GET', 'POST'])
def send_subscription_email(request):
    if request.method == 'POST':
        email = Email(name=request.data['name'],email=request.data['email'],review=request.data['review'], 
                        image = request.data['image'], address = request.data['address'])
        email.save()
        msg = "Thank for your report !!!"
        send_review_email_task.delay(request.data['name'],request.data['email'],request.data['review'])
        return HttpResponse(msg)
    return JsonResponse({"message": "Hello, world!"})



class ReportViewSet(ModelViewSet):
    model = Email
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

