from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import WebinarRegistration
from rest_framework import generics
from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail  

# Form-based view to register for a webinar
def register_webinar(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save()

            # Email sending logic here after form is saved
            send_mail(
                subject='Webinar Registration Confirmation',
                message=f'Thank you for registering for the webinar: {registration.webinar.title}',
                from_email='your-email@example.com',  # Replace with your email
                recipient_list=[registration.email],  # Send email to registered user
                fail_silently=False,
            )

            # Redirect or show a success message
            return redirect('success_page')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# View to list all webinar registrations
def view_registrations(request):
    registrations = WebinarRegistration.objects.all()
    return render(request, 'registrations_list.html', {'registrations': registrations})

# API-based view to list or create webinar registrations
class WebinarRegistrationList(generics.ListCreateAPIView):
    queryset = WebinarRegistration.objects.all()
    serializer_class = RegistrationSerializer

# API-based view for registration (email sent after successful API registration)
class WebinarRegistrationAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            registration = serializer.save()

            # Email sending logic after API registration is saved
            send_mail(
                subject='Webinar Registration Confirmation',
                message=f'Thank you for registering for the webinar: {registration.webinar.title}',
                from_email='your-email@example.com',  # Replace with your email
                recipient_list=[registration.email],  # Send email to registered user
                fail_silently=False,
            )

            # Return a success message and the saved data in the response
            return Response({
                'message': 'Registration successful',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        # If the data is not valid, return errors with a 400 Bad Request status
        return Response({
            'message': 'Registration failed',
            'errors': serializer.errors,
            'data': serializer.data
        }, status=status.HTTP_400_BAD_REQUEST)
