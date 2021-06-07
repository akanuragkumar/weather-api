import re

from django.core.exceptions import ValidationError

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from project_api.models import CityWeatherCollection

from project_api.serializers import (
    CityWeatherCollectionSerializer,
    MailingCollectionSerializer
)
from project_api.constants import regex
from project_api.tasks import email_report
from project_api.pagination import CustomPagination


class CurrentWeatherListView(APIView):
    """Current weather data."""
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = CityWeatherCollectionSerializer
    pagination_class = CustomPagination

    def get(self, request):
        """Method for getting weather-city collection list."""
        objects = CityWeatherCollection.objects.all()
        serializer_class = CityWeatherCollectionSerializer(objects, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        """Method for posting city name."""
        serializer = CityWeatherCollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'New city added to the weather list.'
            })
        # returning validation errors
        return Response({
            'error': serializer.errors
        })


class MailingListView(APIView):
    """Mailing list view"""
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = MailingCollectionSerializer

    def post(self, request):
        """Method for posting emails for weather report."""
        serializer = MailingCollectionSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            for email in request.data.get('emails'):
                if re.search(regex, email):
                    serializer.save()
                    email_report.apply_async(args=(request.data.get('emails'), str(serializer.instance.uuid)))
                    return Response({
                        'status': 'Task Initiated. Please wait for sometime for mail.'
                    })
                else:
                    raise ValidationError('Invalid email address.')
        # returning validation errors
        return Response({
            'error': serializer.errors
        })
